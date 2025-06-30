# main.py

from fastapi import FastAPI, WebSocket
import uvicorn

from speech_to_text import transcribe_audio_chunk
from gpt_stream import stream_gpt_response
from elevenlabs import synthesize_speech
from audio_utils import convert_to_mulaw

from pydub import AudioSegment
import io
import audioop

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Voice Caller is live."}

@app.websocket("/stream")
async def stream_audio(websocket: WebSocket):
    await websocket.accept()
    print("📞 Call connected.")

    try:
        # 🔇 0. Send initial silence to prevent Twilio drop
        silence = AudioSegment.silent(duration=2000)  # 2 seconds
        silence = silence.set_channels(1).set_frame_rate(8000).set_sample_width(2)
        mulaw_silence = audioop.lin2ulaw(silence.raw_data, 2)
        await websocket.send_bytes(mulaw_silence)
        print("📤 Sent initial silence to hold call")

        # 🗣️ 1. AI-generated, human-sounding greeting
        initial_prompt = (
            "Call the person and introduce yourself naturally. "
            "Use a friendly, casual tone. You're calling to assist them with recovering unclaimed surplus funds "
            "from a recent foreclosure. Avoid robotic phrasing. Just say, for example: "
            "'Hi, is this [name]? I’m reaching out because it looks like you're owed some money from a property sale — I may be able to help you claim it.' "
            "Sound like a helpful, professional person, not an AI."
        )

        async for token in stream_gpt_response(initial_prompt):
            async for audio_chunk in synthesize_speech(token):
                mulaw_audio = convert_to_mulaw(audio_chunk)
                await websocket.send_bytes(mulaw_audio)
                print("📤 Sent greeting chunk")
            break  # Send only one full message

        # 🔁 2. Enter user interaction loop
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
                    mulaw_audio = convert_to_mulaw(audio_chunk)
                    await websocket.send_bytes(mulaw_audio)
                    print("📤 Sent response chunk")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("📴 Call disconnected.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
