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
        # 🔇 0. Send valid μ-law silence to prevent Twilio disconnect
        print("🔇 Generating and sending 2s of silence to Twilio...")
        silence = AudioSegment.silent(duration=2000)
        silence = silence.set_channels(1).set_frame_rate(8000).set_sample_width(2)
        raw_pcm = silence.raw_data
        mulaw_silence = audioop.lin2ulaw(raw_pcm, 2)
        await websocket.send_bytes(mulaw_silence)
        print(f"📤 Sent silence chunk of {len(mulaw_silence)} bytes")

        # 🗣️ 1. Send a fast hardcoded greeting with ElevenLabs to buy time
        print("🗣️ Sending fast static ElevenLabs greeting...")
        greeting_text = (
            "Hi, I’m calling about some money that may be owed to you from a property sale. "
            "Do you have a quick minute?"
        )
        async for audio_chunk in synthesize_speech(greeting_text):
            mulaw_audio = convert_to_mulaw(audio_chunk)
            await websocket.send_bytes(mulaw_audio)
            print("📤 Sent static greeting chunk")

        # 🧠 2. Send GPT-generated greeting (overwrites or continues above)
        print("🤖 Generating AI dynamic greeting...")
        initial_prompt = (
            "Call the person and introduce yourself in a helpful, professional way. "
            "You're contacting them because they may be entitled to unclaimed surplus funds from a foreclosure. "
            "Speak clearly and concisely — no need to say you're an AI or use robotic phrasing. "
            "Say something like: 'Hi, I’m calling because it looks like you’re owed some money from a property. I may be able to help you claim it.'"
        )

        async for token in stream_gpt_response(initial_prompt):
            async for audio_chunk in synthesize_speech(token):
                mulaw_audio = convert_to_mulaw(audio_chunk)
                await websocket.send_bytes(mulaw_audio)
                print("📤 Sent GPT greeting chunk")
            break  # Only send first GPT sentence

        # 🔁 3. Conversation loop: listen + respond
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
                    print("📤 Sent GPT response chunk")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("📴 Call disconnected.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
