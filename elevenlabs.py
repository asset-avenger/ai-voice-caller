# elevenlabs.py
import os
import httpx

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

async def synthesize_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.6},
        "model_id": "eleven_multilingual_v2"
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, headers=headers, json=payload) as response:
            async for chunk in response.aiter_bytes():
                yield chunk
