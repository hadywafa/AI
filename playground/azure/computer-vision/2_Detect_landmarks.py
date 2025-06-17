"""
Azure Vision Image Analysis - Landmark Detection
Uses the latest `azure-ai-vision-imageanalysis` SDK.
"""

import os
from typing import List, Optional
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential

# Optional: Load env vars from .env
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Secure credentials from environment
AZURE_VISION_ENDPOINT: Optional[str] = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY: Optional[str] = os.getenv("AZURE_VISION_KEY")

# Sample images to analyze
IMAGES: List[str] = [
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://lh3.googleusercontent.com/p/AF1QipMHftgSCBlvyjxYphi4gLqDC_62WWvZvyy1EBuh=s1360-w1360-h1020",
    "https://assets.editorial.aetnd.com/uploads/2015/02/topic-golden-gate-bridge-gettyimages-177770941.jpg?width=1920&height=960&crop=1920%3A960%2Csmart&quality=75&auto=webp",
    "https://st.depositphotos.com/1759109/1331/i/450/depositphotos_13315503-stock-photo-tower-bridge-at-dusk.jpg",
    "https://images.unsplash.com/photo-1599676603816-0f92b2d713d2?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8dG93ZXIlMjBicmlkZ2V8ZW58MHx8MHx8fDA%3D",
]


def create_image_analysis_client() -> ImageAnalysisClient:
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise EnvironmentError("❌ Missing AZURE_VISION_ENDPOINT or AZURE_VISION_KEY.")
    return ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT, credential=AzureKeyCredential(AZURE_VISION_KEY)
    )


def analyze_landmarks(
    client: ImageAnalysisClient, image_url: str
) -> Optional[ImageAnalysisResult]:
    try:
        result: ImageAnalysisResult = client.analyze_from_url(
            image_url=image_url, visual_features=[VisualFeatures.TAGS], language="en"
        )
        return result
    except Exception as e:
        print(f"\n❌ Error analyzing {image_url}: {e}")
        return None


def extract_landmarks(tags: List) -> List[str]:
    # Simple logic: assume landmark-related tags include 'landmark', 'bridge', etc.
    return [
        tag.name
        for tag in tags
        if "landmark" in tag.name.lower() or "bridge" in tag.name.lower()
    ]


def print_landmark_results(image_url: str, result: ImageAnalysisResult) -> None:
    print(f"\n🖼️ Image: {image_url}")
    if not result.tags or not result.tags.list:
        print("   → No tags detected.")
        return

    landmark_tags: List[str] = extract_landmarks(result.tags.list)
    if landmark_tags:
        print("   → Detected Landmark Tags:")
        for tag in landmark_tags:
            print(f"     • {tag}")
    else:
        print("   → No landmark-related tags found.")


def main() -> None:
    print("🔍 Azure Vision Landmark Detection - Pylance Strict Mode")

    client: ImageAnalysisClient = create_image_analysis_client()

    for image_url in IMAGES:
        result: Optional[ImageAnalysisResult] = analyze_landmarks(client, image_url)
        if result:
            print_landmark_results(image_url, result)


if __name__ == "__main__":
    main()
