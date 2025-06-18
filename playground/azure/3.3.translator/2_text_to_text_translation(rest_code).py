# pip install python-dotenv requests

import os
import uuid
import json
import requests
from dotenv import load_dotenv
from typing import List

# 🔐 Load secrets
load_dotenv()

AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATION_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATION_ENDPOINT")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATION_REGION")

if (
    not AZURE_TRANSLATOR_KEY
    or not AZURE_TRANSLATOR_ENDPOINT
    or not AZURE_TRANSLATOR_REGION
):
    raise EnvironmentError(
        "❌ Azure Translator credentials are missing in the .env file"
    )

TRANSLATE_PATH = "/translate?api-version=3.0"


def translate_text(
    texts: List[str], from_lang: str = "en", to_langs: List[str] = ["ar"]
) -> List[str]:
    """Translate a list of texts using Azure Translator REST API."""
    url = f"{AZURE_TRANSLATOR_ENDPOINT}{TRANSLATE_PATH}&from={from_lang}&to={','.join(to_langs)}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text} for text in texts]

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        print("\n✅ Raw JSON Response:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

        print("\n🌍 Extracted Translations:")
        translations = []
        for item in result:
            for trans in item["translations"]:
                print(f"  → {trans['to']}: {trans['text']}")
                translations.append(trans["text"])
        return translations

    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
        return []
    except KeyError:
        print("❌ Failed to parse translation response.")
        return []


if __name__ == "__main__":
    input_texts = [
        "I am getting confused with all these services. I cannot differentiate between them.",
        "Azure services are very powerful, but I need to learn how to choose the right one.",
    ]
    translated = translate_text(input_texts, from_lang="en", to_langs=["es", "fr"])
