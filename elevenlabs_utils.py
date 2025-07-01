# elevenlabs.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID") or "EXAVITQu4vr4xnSDxMaL"

API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg"
}

def stream_to_speech(text):
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.4,
            "use_speaker_boost": True
        }
    }

    try:
        with httpx.stream("POST", API_URL, headers=headers, json=payload, timeout=30.0) as response:
            response.raise_for_status()
            for chunk in response.iter_bytes():
                if chunk:
                    yield chunk
    except Exception as e:
        print(f"❌ ElevenLabs TTS error: {e}")
        return
