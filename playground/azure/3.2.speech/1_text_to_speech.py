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
VOICE_NAME: str = "ml-IN-MidhunNeural"  # Malayalam male neural voice


def get_speech_config() -> speechsdk.SpeechConfig:
    if not SPEECH_KEY or not SPEECH_REGION:
        raise EnvironmentError("Missing SPEECH_KEY or SPEECH_REGION in environment.")
    config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    config.speech_synthesis_voice_name = VOICE_NAME
    return config


def synthesize_speech(text: str) -> None:
    speech_config = get_speech_config()
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ Speech synthesized successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        print(f"❌ Synthesis canceled: {details.reason}")
        if details.reason == speechsdk.CancellationReason.Error:
            print(f"   ↳ Error details: {details.error_details}")
            print("   ↳ Check your SPEECH_KEY and SPEECH_REGION.")


def main() -> None:
    sample_text = (
        "ഇന്ത്യയിൽ കേരള സംസ്ഥാനത്തിലും ഭാഗികമായി കേന്ദ്രഭരണ പ്രദേശങ്ങളായ ലക്ഷദ്വീപിലും പോണ്ടിച്ചേരിയുടെ ഭാഗമായ മാഹിയിലും "
        "തമിഴ്നാട്ടിലെ കന്യാകുമാരി ജില്ലയിലും നീലഗിരി ജില്ലയിലെ ഗൂഡല്ലൂർ താലൂക്കിലും സംസാരിക്കപ്പെടുന്ന ഭാഷയാണ് മലയാളം."
    )
    print("🗣️ Synthesizing Malayalam text...\n")
    synthesize_speech(sample_text)


if __name__ == "__main__":
    main()
