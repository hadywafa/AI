import os
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load Azure Speech credentials from environment
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")


def read_ssml_file(file_path: str) -> str:
    """Reads SSML content from an XML file."""
    absolute_path = Path(file_path).resolve()
    if not absolute_path.exists():
        raise FileNotFoundError(f"SSML file not found: {absolute_path}")
    with open(absolute_path, mode="r", encoding="utf-8") as file:
        return file.read()


def get_speech_synthesizer() -> speechsdk.SpeechSynthesizer:
    """Get Speech Synthesizer"""

    if not SPEECH_KEY or not SPEECH_REGION:
        raise EnvironmentError("Missing SPEECH_KEY or SPEECH_REGION in environment.")

    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION
    )
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    return synthesizer


def synthesize_ssml(ssml_content: str) -> None:
    """Synthesizes speech from an SSML string."""
    synthesizer = get_speech_synthesizer()

    result = synthesizer.speak_ssml_async(ssml_content).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ Speech synthesized successfully from SSML.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"❌ Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"   ↳ Error: {cancellation_details.error_details}")
            print("   ↳ Check your Azure Speech key/region or malformed SSML.")


if __name__ == "__main__":
    try:
        ssml_path = os.path.join(
            os.path.dirname(__file__), "azure_speech_SSML_resources/ssml8.xml"
        )
        ssml = read_ssml_file(ssml_path)
        synthesize_ssml(ssml)
    except Exception as ex:
        print(f"💥 Exception: {ex}")
