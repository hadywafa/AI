"""
Azure AI Content Safety - Image Analysis
Refactored by OpenAI ChatGPT
"""

import os
from pathlib import Path
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

# Optional: load from .env file (if using python-dotenv)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# ✅ Load secrets securely from env
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")


def get_image_path(filename: str) -> Path:
    """Resolve absolute path to the image file."""
    return Path(__file__).resolve().parent / "sample_data" / filename


def create_contentsafety_client() -> ContentSafetyClient:
    """Initialize and return the ContentSafety client."""
    if not AZURE_CONTENT_SAFETY_KEY or not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise EnvironmentError("Azure credentials not found in environment variables.")

    return ContentSafetyClient(
        AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )


def analyze_image_file(image_path: Path) -> Optional[dict]:
    """Analyze an image using Azure AI Content Safety."""
    client = create_contentsafety_client()

    try:
        with image_path.open("rb") as file:
            image_data = ImageData(content=file.read())
            request = AnalyzeImageOptions(image=image_data)
            response = client.analyze_image(request)

        # Extract categories

        # results = {
        #     item.category: item.severity for item in response.categories_analysis
        # }

        results = {
            (
                item.category.name
                if isinstance(item.category, ImageCategory)
                else item.category
            ): item.severity
            for item in response.categories_analysis
        }

        return results

    except HttpResponseError as e:
        print("[ERROR] Image analysis failed.")
        if e.error:
            print(f" → Code: {e.error.code}")
            print(f" → Message: {e.error.message}")
        else:
            print(e)
        return None


def print_analysis_results(results: dict) -> None:
    """Print the severity levels for each category."""
    print("\n--- Analysis Results ---")
    for category in ImageCategory:
        severity = results.get(category.value)
        if severity is not None:
            print(f"{category.name}: Severity {severity}")
        else:
            print(f"{category.name}: Not detected")


def main():
    image_path = get_image_path("porn-image.jpg")
    print(f"Analyzing image: {image_path}")

    results = analyze_image_file(image_path)
    if results:
        print_analysis_results(results)
    else:
        print("Image analysis failed or returned no results.")


if __name__ == "__main__":
    main()
