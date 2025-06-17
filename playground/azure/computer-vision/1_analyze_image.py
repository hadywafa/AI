"""
Azure AI Vision - Image Analysis Example
Features: Tagging, Captioning, Reading, Smart Crops, People & Object Detection
"""

import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load credentials securely
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

# Default image URL (can be replaced with dynamic input or CLI)
DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQykzoZeCE0p7LeuyHnLYCdPP2jju9d5PaMeA&s"


def create_vision_client() -> ImageAnalysisClient:
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise EnvironmentError("Azure Vision endpoint or key is missing.")
    return ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT, credential=AzureKeyCredential(AZURE_VISION_KEY)
    )


def analyze_image_from_url(client: ImageAnalysisClient, image_url: str) -> None:
    visual_features = [
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
        VisualFeatures.CAPTION,
        VisualFeatures.DENSE_CAPTIONS,
        VisualFeatures.READ,
        VisualFeatures.SMART_CROPS,
        VisualFeatures.PEOPLE,
    ]

    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=visual_features,
        smart_crops_aspect_ratios=[0.9, 1.33],
        gender_neutral_caption=True,
        language="en",
    )

    print("\n📸 Image Analysis Results:\n")

    if result.caption:
        print("📝 Caption:")
        print(
            f"   → '{result.caption.text}' (Confidence: {result.caption.confidence:.4f})"
        )

    if result.dense_captions:
        print("\n🔍 Dense Captions:")
        for caption in result.dense_captions.list:
            print(
                f"   → '{caption.text}' at {caption.bounding_box} (Confidence: {caption.confidence:.4f})"
            )

    if result.read and result.read.blocks:
        print("\n📖 Read (OCR):")
        for block in result.read.blocks:
            for line in block.lines:
                print(f"   Line: '{line.text}' at {line.bounding_polygon}")
                for word in line.words:
                    print(
                        f"     Word: '{word.text}' at {word.bounding_polygon} (Confidence: {word.confidence:.4f})"
                    )

    if result.tags:
        print("\n🏷️ Tags:")
        for tag in result.tags.list:
            print(f"   → '{tag.name}' (Confidence: {tag.confidence:.4f})")

    if result.objects:
        print("\n📦 Objects:")
        for obj in result.objects.list:
            tag = obj.tags[0]
            print(
                f"   → '{tag.name}' at {obj.bounding_box} (Confidence: {tag.confidence:.4f})"
            )

    if result.people:
        print("\n🧑 People:")
        for person in result.people.list:
            print(
                f"   → Bounding box: {person.bounding_box} (Confidence: {person.confidence:.4f})"
            )

    if result.smart_crops:
        print("\n📐 Smart Crops:")
        for crop in result.smart_crops.list:
            print(
                f"   → Aspect Ratio {crop.aspect_ratio}: Crop Area {crop.bounding_box}"
            )

    print("\n🖼️ Metadata:")
    print(f"   → Image Size: {result.metadata.width}x{result.metadata.height}")
    print(f"   → Model Version: {result.model_version}")


def main():
    print("🔎 Starting Azure AI Image Analysis...")
    client = create_vision_client()
    analyze_image_from_url(client, DEFAULT_IMAGE_URL)


if __name__ == "__main__":
    main()
