import os
import uuid
import time
from typing import List, Optional

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
    Tag,
    Project,
    Iteration,
)
from msrest.authentication import ApiKeyCredentials

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Environment configuration
TRAINING_ENDPOINT: Optional[str] = os.getenv("AZURE_CUSTOMVISION_TRAINING_ENDPOINT")
TRAINING_KEY: Optional[str] = os.getenv("AZURE_CUSTOMVISION_TRAINING_KEY")
PREDICTION_ENDPOINT: Optional[str] = os.getenv("AZURE_CUSTOMVISION_PREDICTION_ENDPOINT")
PREDICTION_KEY: Optional[str] = os.getenv("AZURE_CUSTOMVISION_PREDICTION_KEY")
PREDICTION_RESOURCE_ID: Optional[str] = os.getenv(
    "AZURE_CUSTOMVISION_PREDICTION_RESOURCE_ID"
)
PUBLISH_NAME: str = "classifyModel"
IMAGE_ROOT_DIR: str = os.path.join(os.path.dirname(__file__), "image_classification_resources")


def get_trainer() -> CustomVisionTrainingClient:
    if not TRAINING_ENDPOINT or not TRAINING_KEY:
        raise EnvironmentError("Missing training endpoint or key.")
    return CustomVisionTrainingClient(
        endpoint=TRAINING_ENDPOINT,
        credentials=ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY}),
    )


def get_predictor() -> CustomVisionPredictionClient:
    if not PREDICTION_ENDPOINT or not PREDICTION_KEY:
        raise EnvironmentError("Missing prediction endpoint or key.")
    return CustomVisionPredictionClient(
        endpoint=PREDICTION_ENDPOINT,
        credentials=ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY}),
    )


def clean_all_projects(trainer: CustomVisionTrainingClient) -> None:
    print("🧹 Cleaning existing projects...")
    for project in trainer.get_projects():
        for iteration in trainer.get_iterations(project.id):
            trainer.unpublish_iteration(
                project_id=project.id, iteration_id=iteration.id
            )
        trainer.delete_project(project.id)


def create_and_tag_project(
    trainer: CustomVisionTrainingClient,
) -> tuple[Project, Tag, Tag]:
    print("🛠️ Creating project...")
    project_name: str = f"FlowerClassifier-{uuid.uuid4()}"
    project: Project = trainer.create_project(project_name)
    hemlock_tag: Tag = trainer.create_tag(project.id, "Hemlock")
    cherry_tag: Tag = trainer.create_tag(project.id, "Japanese Cherry")
    return project, hemlock_tag, cherry_tag


def load_images_for_tag(
    tag_name: str, count: int, tag_id: str
) -> List[ImageFileCreateEntry]:
    entries: List[ImageFileCreateEntry] = []
    for i in range(1, count + 1):
        file_path = os.path.join(
            IMAGE_ROOT_DIR,
            tag_name.replace(" ", "_"),
            f"{tag_name.lower().replace(' ', '_')}_{i}.jpg",
        )
        with open(file_path, "rb") as f:
            entries.append(
                ImageFileCreateEntry(
                    name=os.path.basename(file_path),
                    contents=f.read(),
                    tag_ids=[tag_id],
                )
            )
    return entries


def upload_images(
    trainer: CustomVisionTrainingClient,
    project_id: str,
    hemlock_tag: Tag,
    cherry_tag: Tag,
) -> None:
    print("📤 Uploading images...")
    images: List[ImageFileCreateEntry] = []
    images.extend(load_images_for_tag("Hemlock", 10, hemlock_tag.id))
    images.extend(load_images_for_tag("Japanese Cherry", 10, cherry_tag.id))

    upload_result = trainer.create_images_from_files(
        project_id, ImageFileCreateBatch(images=images)
    )
    if not upload_result.is_batch_successful:
        raise RuntimeError(
            "❌ Image upload failed: "
            + ", ".join([img.status for img in upload_result.images])
        )


def train_and_publish_model(
    trainer: CustomVisionTrainingClient, project: Project
) -> Iteration:
    print("🧠 Training model...")
    iteration: Iteration = trainer.train_project(project.id)
    while iteration.status != "Completed":
        print(f"⏳ Training status: {iteration.status}... waiting 10s")
        time.sleep(10)
        iteration = trainer.get_iteration(project.id, iteration.id)

    print("✅ Training complete. Publishing...")
    trainer.publish_iteration(
        project.id, iteration.id, PUBLISH_NAME, PREDICTION_RESOURCE_ID
    )
    return iteration


def run_prediction(predictor: CustomVisionPredictionClient, project_id: str) -> None:
    print("🔍 Running prediction on test image...")
    test_image_path = os.path.join(IMAGE_ROOT_DIR, "Test", "test_image.jpg")
    with open(test_image_path, "rb") as image_data:
        results = predictor.classify_image(project_id, PUBLISH_NAME, image_data.read())
        print("📈 Prediction Results:")
        for prediction in results.predictions:
            print(f"  • {prediction.tag_name}: {prediction.probability * 100:.2f}%")


def main() -> None:
    trainer = get_trainer()
    clean_all_projects(trainer)
    project, hemlock_tag, cherry_tag = create_and_tag_project(trainer)
    upload_images(trainer, project.id, hemlock_tag, cherry_tag)
    train_and_publish_model(trainer, project)
    predictor = get_predictor()
    run_prediction(predictor, project.id)


if __name__ == "__main__":
    main()
