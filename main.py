from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import PlainTextResponse
import uvicorn
import os

from audio_utils import convert_to_mulaw
from speech_to_text import transcribe_audio_chunk
from gpt_stream import stream_gpt_response
from elevenlabs_utils import stream_to_speech

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Voice Caller is live."}

@app.post("/voice")
async def voice_handler(request: Request):
    # This returns TwiML that starts a <Stream> to your WebSocket server
    stream_url = os.getenv("RENDER_STREAM_URL")
    response = f"""
    <Response>
        <Start>
            <Stream url="{stream_url}" />
        </Start>
    </Response>
    """
    return PlainTextResponse(content=response.strip(), media_type="text/xml")

@app.websocket("/stream")
async def stream_audio(websocket: WebSocket):
    await websocket.accept()
    print("📞 Call connected.")

    try:
        while True:
            data = await websocket.receive_bytes()

            # Transcribe caller's audio
            transcript = transcribe_audio_chunk(data)
            print(f"📝 User: {transcript}")

            # GPT response + convert to speech
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
