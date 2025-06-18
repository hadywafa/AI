import os
import uuid
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Environment variable keys
AZURE_TRANSLATION_KEY = os.getenv("AZURE_TRANSLATION_KEY")
AZURE_TRANSLATION_ENDPOINT = os.getenv("AZURE_TRANSLATION_ENDPOINT")
AZURE_TRANSLATION_REGION = os.getenv("AZURE_TRANSLATION_REGION")

# Constants
API_VERSION = "3.0"
SOURCE_LANGUAGE = "en"
TARGET_LANGUAGE = "ar"

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "document" / "test.txt"
OUTPUT_FILE = BASE_DIR / "document" / "document_translated.txt"


def build_translation_url() -> str:
    """Constructs the full translation endpoint URL."""
    path = f"/translate?api-version={API_VERSION}&from={SOURCE_LANGUAGE}&to={TARGET_LANGUAGE}"
    return f"{AZURE_TRANSLATION_ENDPOINT.rstrip('/')}{path}"


def build_headers() -> dict:
    """Creates headers for the Azure Translator API request."""
    return {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATION_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATION_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }


def translate_text(text: str) -> str:
    """Sends a request to the Azure Translator API and returns the translated text."""
    url = build_translation_url()
    headers = build_headers()
    body = [{"text": text}]

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Raise HTTPError on failure

    data = response.json()
    return data[0]["translations"][0]["text"]


def translate_document(input_path: str, output_path: str) -> None:
    """Reads a file, translates its content, and writes the result to another file."""
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            original_text = infile.read()

        translated_text = translate_text(original_text)

        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(translated_text)

        print("✅ Document translated successfully.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    translate_document(INPUT_FILE, OUTPUT_FILE)
