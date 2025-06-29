# main.py
from fastapi import FastAPI, WebSocket
import uvicorn

from speech_to_text import transcribe_audio_chunk
from gpt_stream import stream_gpt_response
from elevenlabs import synthesize_speech
from audio_utils import convert_to_mulaw

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Voice Caller is live."}

@app.websocket("/stream")
async def stream_audio(websocket: WebSocket):
    await websocket.accept()
    print("📞 Call connected.")

    try:
        while True:
            data = await websocket.receive_bytes()
            print(f"🎙️ Received audio chunk: {len(data)} bytes")

            transcript = transcribe_audio_chunk(data)
            print(f"📝 Transcript: {transcript}")

            if not transcript:
                continue

            async for token in stream_gpt_response(transcript):
                print(f"🤖 GPT Token: {token}", end="")

                async for audio_chunk in synthesize_speech(token):
                    if not audio_chunk:
                        continue

                    mulaw_audio = convert_to_mulaw(audio_chunk)
                    await websocket.send_bytes(mulaw_audio)
                    print(f"📤 Sent μ-law audio chunk to Twilio")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("📴 Call disconnected.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
