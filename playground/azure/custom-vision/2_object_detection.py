import os
import time
import uuid
from typing import Dict, List, Tuple

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateEntry,
    ImageFileCreateBatch,
    Region,
    Tag,
    Iteration,
    Project,
)
from msrest.authentication import ApiKeyCredentials

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load configuration
TRAINER_ENDPOINT = os.getenv("AZURE_CUSTOMVISION_TRAINING_ENDPOINT")
TRAINING_KEY = os.getenv("AZURE_CUSTOMVISION_TRAINING_KEY")
PREDICTION_ENDPOINT = os.getenv("AZURE_CUSTOMVISION_PREDICTION_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_CUSTOMVISION_PREDICTION_KEY")
PREDICTION_RESOURCE_ID = os.getenv("AZURE_CUSTOMVISION_PREDICTION_RESOURCE_ID")

PUBLISH_NAME = "detectModel"
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "object_detection_resources")


def get_clients() -> Tuple[CustomVisionTrainingClient, CustomVisionPredictionClient]:
    if not (
        TRAINER_ENDPOINT
        and TRAINING_KEY
        and PREDICTION_KEY
        and PREDICTION_ENDPOINT
        and PREDICTION_RESOURCE_ID
    ):
        raise EnvironmentError("Missing Azure Custom Vision credentials or endpoints.")

    trainer = CustomVisionTrainingClient(
        TRAINER_ENDPOINT, ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
    )
    predictor = CustomVisionPredictionClient(
        PREDICTION_ENDPOINT,
        ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY}),
    )
    return trainer, predictor


def cleanup_projects(trainer: CustomVisionTrainingClient) -> None:
    for project in trainer.get_projects():
        for iteration in trainer.get_iterations(project.id):
            trainer.unpublish_iteration(project.id, iteration.id)
        trainer.delete_project(project.id)


def create_project_with_tags(
    trainer: CustomVisionTrainingClient,
) -> Tuple[Project, Tag, Tag]:
    domain = next(
        d
        for d in trainer.get_domains()
        if d.type == "ObjectDetection" and d.name == "General"
    )
    project_name = f"ObjectDetection-{uuid.uuid4()}"
    project = trainer.create_project(project_name, domain_id=domain.id)
    fork_tag = trainer.create_tag(project.id, "fork")
    scissors_tag = trainer.create_tag(project.id, "scissors")
    return project, fork_tag, scissors_tag


def prepare_images_with_regions(
    label: str, tag_id: str, region_data: Dict[str, List[float]], base_dir: str
) -> List[ImageFileCreateEntry]:
    entries: List[ImageFileCreateEntry] = []
    label_folder = os.path.join(base_dir, label)

    for file_name, (left, top, width, height) in region_data.items():
        image_path = os.path.join(label_folder, f"{file_name}.jpg")
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Missing image: {image_path}")
        with open(image_path, "rb") as f:
            region = Region(
                tag_id=tag_id, left=left, top=top, width=width, height=height
            )
            entry = ImageFileCreateEntry(
                name=file_name, contents=f.read(), regions=[region]
            )
            entries.append(entry)
    return entries


def upload_images(
    trainer: CustomVisionTrainingClient,
    project_id: str,
    fork_tag: Tag,
    scissors_tag: Tag,
    fork_regions: Dict[str, List[float]],
    scissors_regions: Dict[str, List[float]],
) -> None:
    print("📤 Uploading tagged images...")
    entries = []
    entries += prepare_images_with_regions("fork", fork_tag.id, fork_regions, IMAGE_DIR)
    entries += prepare_images_with_regions(
        "scissors", scissors_tag.id, scissors_regions, IMAGE_DIR
    )

    upload_result = trainer.create_images_from_files(
        project_id, ImageFileCreateBatch(images=entries)
    )
    if not upload_result.is_batch_successful:
        for img in upload_result.images:
            print(f"Failed: {img.status}")
        raise RuntimeError("❌ Image upload failed.")


def train_model(trainer: CustomVisionTrainingClient, project_id: str) -> Iteration:
    print("🧠 Training model...")
    iteration = trainer.train_project(project_id)
    while iteration.status != "Completed":
        print(f"⏳ Training status: {iteration.status} (waiting 2s)")
        time.sleep(2)
        iteration = trainer.get_iteration(project_id, iteration.id)
    print("✅ Training complete.")
    trainer.publish_iteration(
        project_id, iteration.id, PUBLISH_NAME, PREDICTION_RESOURCE_ID
    )
    return iteration


def predict(predictor: CustomVisionPredictionClient, project_id: str) -> None:
    print("🔍 Predicting...")
    test_image_path = os.path.join(IMAGE_DIR, "test", "test_image.jpg")
    with open(test_image_path, "rb") as test_data:
        results = predictor.detect_image(project_id, PUBLISH_NAME, test_data.read())

    print("📈 Prediction Results:")
    for p in results.predictions:
        print(
            f"  • {p.tag_name}: {p.probability * 100:.2f}% "
            f"(left={p.bounding_box.left:.2f}, top={p.bounding_box.top:.2f}, "
            f"width={p.bounding_box.width:.2f}, height={p.bounding_box.height:.2f})"
        )


def main():
    trainer, predictor = get_clients()
    cleanup_projects(trainer)
    project, fork_tag, scissors_tag = create_project_with_tags(trainer)

    from object_detection_resources.region_data import (
        fork_image_regions,
        scissors_image_regions,
    )

    upload_images(
        trainer,
        project.id,
        fork_tag,
        scissors_tag,
        fork_image_regions,
        scissors_image_regions,
    )
    train_model(trainer, project.id)
    predict(predictor, project.id)


if __name__ == "__main__":
    main()
