"""
Azure AI Content Safety - Text Analysis
Refactored by OpenAI ChatGPT
"""

import os
from typing import Optional, Dict

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Optional: load from .env file (if using python-dotenv)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load from environment variables
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")


def create_contentsafety_client() -> ContentSafetyClient:
    """Initialize and return the Content Safety client."""
    if not AZURE_CONTENT_SAFETY_KEY or not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise EnvironmentError("Azure Content Safety credentials not set.")

    return ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY),
    )


def analyze_text_content(text: str) -> Optional[Dict[str, int]]:
    """Analyze text for harmful content categories."""
    client = create_contentsafety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("[ERROR] Text analysis failed.")
        if e.error:
            print(f" → Code: {e.error.code}")
            print(f" → Message: {e.error.message}")
        else:
            print(e)
        return None

    return {
        (
            item.category.name
            if isinstance(item.category, TextCategory)
            else item.category
        ): item.severity
        for item in response.categories_analysis
        if item.severity is not None
    }


def print_analysis_results(results: Dict[str, int]) -> None:
    """Pretty print severity of detected categories."""
    print("\n--- Text Analysis Results ---")
    for category in TextCategory:
        severity = results.get(category.value)  # ✅ Use .value to match keys
        if severity is not None:
            print(f"{category.name}: Severity {severity}")
        else:
            print(f"{category.name}: Not detected")


def main():
    sample_text = "You are an idiot. I will kill you."
    print(f'Analyzing text: "{sample_text}"\n')

    results = analyze_text_content(sample_text)

    if results:
        print_analysis_results(results)
    else:
        print("No results or analysis failed.")


if __name__ == "__main__":
    main()
