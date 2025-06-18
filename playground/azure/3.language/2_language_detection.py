import os
from typing import List, Optional

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load from environment
AZURE_LANGUAGE_ENDPOINT: Optional[str] = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_LANGUAGE_KEY: Optional[str] = os.getenv("AZURE_LANGUAGE_KEY")


def get_client() -> TextAnalyticsClient:
    if not AZURE_LANGUAGE_ENDPOINT or not AZURE_LANGUAGE_KEY:
        raise EnvironmentError("Missing AZURE_LANGUAGE_ENDPOINT or AZURE_LANGUAGE_KEY.")
    credential = AzureKeyCredential(AZURE_LANGUAGE_KEY)
    return TextAnalyticsClient(endpoint=AZURE_LANGUAGE_ENDPOINT, credential=credential)


def detect_language(client: TextAnalyticsClient, texts: List[str]) -> None:
    try:
        results = client.detect_language(documents=texts, country_hint="us")
        for idx, result in enumerate(results):
            if not result.is_error:
                print(
                    f"📄 Document {idx + 1}: Language = {result.primary_language.name}"
                )
            else:
                print(f"❌ Document {idx + 1} error: {result.error}")
    except Exception as ex:
        print(f"⚠️ Exception during language detection: {ex}")


def main() -> None:
    client = get_client()
    sample_texts = ["നിനക്ക് സ്വാഗതം."]
    detect_language(client, sample_texts)


if __name__ == "__main__":
    main()
