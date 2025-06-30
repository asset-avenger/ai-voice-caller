# main.py
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

from audio_utils import convert_to_mulaw
from speech_to_text import transcribe_audio_chunk
from gpt_stream import stream_gpt_response
from elevenlabs_utils import stream_to_speech

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

            # Decode & transcribe the audio
            transcript = transcribe_audio_chunk(data)
            print(f"📝 Transcript: {transcript}")

            # Get GPT response stream
            async for chunk in stream_gpt_response(transcript):
                print(f"🤖 GPT: {chunk}")
                audio_chunk = stream_to_speech(chunk)

                if audio_chunk:
                    await websocket.send_bytes(audio_chunk)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("📴 Call disconnected.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
