import os
from typing import Optional
import azure.cognitiveservices.speech as speechsdk

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load from environment
SPEECH_KEY: Optional[str] = os.getenv("SPEECH_KEY")
SPEECH_REGION: Optional[str] = os.getenv("SPEECH_REGION")


def get_speech_recognizer(language: str = "en-US") -> speechsdk.SpeechRecognizer:
    if not SPEECH_KEY or not SPEECH_REGION:
        raise EnvironmentError("Missing SPEECH_KEY or SPEECH_REGION in environment.")

    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION
    )
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )


def recognize_speech_from_microphone() -> None:
    recognizer = get_speech_recognizer()
    print("🎙️ Speak something into your microphone...")

    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"✅ Recognized: {result.text}")

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ No speech recognized.")
        print(f"   ↳ NoMatch details: {result.no_match_details}")

    elif result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        print(f"❌ Recognition canceled: {details.reason}")
        if details.reason == speechsdk.CancellationReason.Error:
            print(f"   ↳ Error details: {details.error_details}")
            print("   ↳ Check SPEECH_KEY and SPEECH_REGION values.")


def main():
    recognize_speech_from_microphone()


if __name__ == "__main__":
    main()
