# pip install azure-ai-translation-text python-dotenv

import os
from dotenv import load_dotenv
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# 🔄 Load environment variables from .env file
load_dotenv()

AZURE_TRANSLATION_KEY = os.getenv("AZURE_TRANSLATION_KEY")
AZURE_TRANSLATION_ENDPOINT = os.getenv("AZURE_TRANSLATION_ENDPOINT")
AZURE_TRANSLATION_REGION = os.getenv("AZURE_TRANSLATION_REGION")

# 🧠 Validate env vars
if (
    not AZURE_TRANSLATION_KEY
    or not AZURE_TRANSLATION_ENDPOINT
    or not AZURE_TRANSLATION_REGION
):
    raise EnvironmentError("❌ Missing Azure Translation credentials in .env")

# ✅ Initialize Translation Client
credential = AzureKeyCredential(AZURE_TRANSLATION_KEY)
translator = TextTranslationClient(
    endpoint=AZURE_TRANSLATION_ENDPOINT,
    credential=credential,
    region=AZURE_TRANSLATION_REGION,
)


def print_supported_languages() -> None:
    """Prints all supported languages for translation, transliteration, and dictionary."""
    try:
        response = translator.get_supported_languages()

        print("\n📚 Supported Languages:")
        print(f"  • Translation: {len(response.translation or {})}")
        print(f"  • Transliteration: {len(response.transliteration or {})}")
        print(f"  • Dictionary: {len(response.dictionary or {})}")

        if response.translation:
            print("\n🌐 Translation Languages:")
            for lang, info in response.translation.items():
                print(f"  - {lang}: {info.name} ({info.native_name})")

    except HttpResponseError as ex:
        print(
            f"\n❌ Error getting supported languages: {ex.error.code} - {ex.error.message}"
        )


def translate_text(texts: list[str], to_languages: list[str]) -> None:
    """Translates a list of texts to the given target languages."""
    try:
        input_items = [InputTextItem(text=t) for t in texts]
        response = translator.translate(body=input_items, to_language=to_languages)

        if not response:
            print("⚠️ No translation response returned.")
            return

        translation = response[0]
        if translation.detected_language:
            print(
                f"\n🔍 Detected Language: {translation.detected_language.language} "
                f"(Confidence: {translation.detected_language.score:.2f})"
            )

        print("\n📤 Translation Results:")
        for trans in translation.translations:
            print(f"  → [{trans.to}] {trans.text}")

    except HttpResponseError as ex:
        print(f"\n❌ Translation error: {ex.error.code} - {ex.error.message}")


if __name__ == "__main__":
    print("🔧 Azure Text Translation Demo with .env 🔐")
    # print_supported_languages()
    translate_text(["This is a test."], ["ar", "fr"])
