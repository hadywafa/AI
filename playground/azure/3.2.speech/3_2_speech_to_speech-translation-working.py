import os
from typing import Optional
import azure.cognitiveservices.speech as speechsdk

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load securely from env or fallback
SPEECH_KEY: Optional[str] = os.getenv("SPEECH_KEY")
SPEECH_REGION: Optional[str] = os.getenv("SPEECH_REGION")


def create_translation_recognizer(
    subscription: str, region: str, source_lang: str = "en-US", target_lang: str = "it"
) -> speechsdk.translation.TranslationRecognizer:
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=subscription,
        region=region,
        speech_recognition_language=source_lang,
    )
    translation_config.add_target_language(target_lang)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config
    )


def synthesize_speech(
    subscription: str, region: str, text: str, voice: Optional[str] = None
) -> None:
    speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)

    if voice:
        speech_config.speech_synthesis_voice_name = voice

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ Translation synthesized to speech successfully.")
    else:
        print("❌ Synthesis failed.")
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"   ↳ Reason: {cancellation.reason}")
            print(f"   ↳ Details: {cancellation.error_details}")


def translate_speech_to_speech(
    subscription: str, region: str, source_lang: str = "en-US", target_lang: str = "it"
) -> None:
    recognizer = create_translation_recognizer(
        subscription, region, source_lang, target_lang
    )

    print(f"🎙️ Say something in {source_lang} to translate to {target_lang.upper()}...")

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        translated = result.translations.get(target_lang, "")
        print(f"✅ Recognized: {result.text}")
        print(f"🌐 Translated ({target_lang.upper()}): {translated}")
        synthesize_speech(subscription, region, translated)

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ No speech could be recognized.")

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print("❌ Translation canceled.")
        print(f"   ↳ Reason: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"   ↳ Error: {cancellation.error_details}")


if __name__ == "__main__":
    translate_speech_to_speech(SPEECH_KEY, SPEECH_REGION)
