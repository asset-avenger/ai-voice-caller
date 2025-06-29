# speech_to_text.py
import os
import io
import json
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

if os.getenv("GOOGLE_CLOUD_SPEECH_CREDENTIALS_JSON"):
    creds_dict = json.loads(os.getenv("GOOGLE_CLOUD_SPEECH_CREDENTIALS_JSON"))
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
else:
    credentials = None

client = speech.SpeechClient(credentials=credentials)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MULAW,
    sample_rate_hertz=8000,
    language_code="en-US",
    use_enhanced=True,
    model="phone_call"
)

def transcribe_audio_chunk(audio_chunk: bytes) -> str:
    audio = speech.RecognitionAudio(content=audio_chunk)
    response = client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript
    return ""
