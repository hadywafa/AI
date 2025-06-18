# 4_transliteration.py — Arabic example

import os
import uuid
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict

# 🔐 Load credentials from .env
load_dotenv()

AZURE_TRANSLATION_KEY = os.getenv("AZURE_TRANSLATION_KEY")
AZURE_TRANSLATION_ENDPOINT = os.getenv("AZURE_TRANSLATION_ENDPOINT")
AZURE_TRANSLATION_REGION = os.getenv("AZURE_TRANSLATION_REGION")

# 🔧 Configuration
API_VERSION = "3.0"
LANGUAGE = "ar"  # Arabic language
FROM_SCRIPT = "Arab"  # Arabic script
TO_SCRIPT = "Latn"  # Latin script


def build_transliteration_url() -> str:
    """Builds the Azure Translator transliteration endpoint URL."""
    base = AZURE_TRANSLATION_ENDPOINT.rstrip("/")
    return f"{base}/transliterate?api-version={API_VERSION}&language={LANGUAGE}&fromScript={FROM_SCRIPT}&toScript={TO_SCRIPT}"


def build_headers() -> Dict[str, str]:
    """Creates request headers for the transliteration API."""
    return {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATION_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATION_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }


def transliterate_text(texts: List[str]) -> List[str]:
    """Calls the transliteration API and returns transliterated text."""
    url = build_transliteration_url()
    headers = build_headers()
    body = [{"Text": text} for text in texts]

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        print("\n✅ Raw JSON Response:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

        print("\n🔤 Transliterated Output:")
        return [item["text"] for item in result]

    except requests.RequestException as e:
        print(f"\n❌ Request error: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"\n❌ Failed to parse result: {e}")
        return []


if __name__ == "__main__":
    input_texts = ["استخدام", "السلام عليكم", "برمجة الحاسوب"]

    outputs = transliterate_text(input_texts)

    for i, result in enumerate(outputs, start=1):
        print(f"  {i}. {result}")
