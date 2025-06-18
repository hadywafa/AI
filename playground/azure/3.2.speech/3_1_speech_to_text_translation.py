import os
from typing import Optional
import azure.cognitiveservices.speech as speechsdk

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load credentials securely
SPEECH_KEY: Optional[str] = os.getenv("SPEECH_KEY")
SPEECH_REGION: Optional[str] = os.getenv("SPEECH_REGION")


def get_translation_recognizer(
    source_lang: str = "en-US", target_lang: str = "ml"
) -> speechsdk.translation.TranslationRecognizer:
    if not SPEECH_KEY or not SPEECH_REGION:
        raise EnvironmentError("Missing SPEECH_KEY or SPEECH_REGION in environment.")

    config = speechsdk.translation.SpeechTranslationConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION
    )
    config.speech_recognition_language = source_lang
    config.add_target_language(target_lang)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.translation.TranslationRecognizer(
        translation_config=config, audio_config=audio_config
    )


def translate_speech_from_microphone(
    source_lang: str = "en-US", target_lang: str = "ml"
) -> None:
    recognizer = get_translation_recognizer(source_lang, target_lang)

    print("🎙️ Speak into your microphone...")
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print(f"✅ Recognized: {result.text}")
        print(f"🌐 Translated ({target_lang}): {result.translations[target_lang]}")

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ No speech could be recognized.")
        print(f"   ↳ Details: {result.no_match_details}")

    elif result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        print(f"❌ Recognition canceled: {details.reason}")
        if details.reason == speechsdk.CancellationReason.Error:
            print(f"   ↳ Error details: {details.error_details}")
            print("   ↳ Check your SPEECH_KEY and SPEECH_REGION.")


def main():
    translate_speech_from_microphone()


if __name__ == "__main__":
    main()
