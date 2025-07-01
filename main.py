import os
import json
import asyncio
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
from typing import Dict, Any

load_dotenv()

app = FastAPI()
STREAM_URL = os.getenv("RENDER_STREAM_URL")  # e.g. "wss://.../stream"

@app.post("/voice")
async def voice_handler(request: Request):
    # Immediately begin streaming media to our /stream websocket
    vr = VoiceResponse()
    vr.start()
    vr.append(Stream(url=STREAM_URL))
    # No Say—ElevenLabs will speak via the stream
    return PlainTextResponse(content=str(vr), media_type="text/xml")

@app.websocket("/stream")
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:
        # Send initial Headers if needed (depends on ElevenLabs API)
        # Receive Twilio media frames and forward to ElevenLabs
        eleven_ws = await connect_to_elevenlabs()
        async def twilio_to_eleven():
            while True:
                msg = await ws.receive_text()
                data = json.loads(msg)
                if data.get("event") == "start":
                    continue
                if data.get("event") == "media":
                    audio_payload = data["media"]["payload"]
                    await eleven_ws.send(audio_payload)
                if data.get("event") == "stop":
                    await eleven_ws.send("EOS")
                    break
        async def eleven_to_twilio():
            while True:
                chunk = await eleven_ws.recv()
                # Wrap raw audio in Twilio MediaStreamAudioFrame
                frame = json.dumps({"event": "media", "media": {"payload": chunk}})
                await ws.send_text(frame)
        await asyncio.gather(twilio_to_eleven(), eleven_to_twilio())
    except WebSocketDisconnect:
        pass
    finally:
        await ws.close()

async def connect_to_elevenlabs():
    # Replace this with actual ElevenLabs WebSocket handshake
    import websockets
    url = os.getenv("ELEVENLABS_WS_URL")
    headers = {"Authorization": f"Bearer {os.getenv('ELEVENLABS_API_KEY')}"}
    return await websockets.connect(url, extra_headers=headers)

@app.get("/")
async def root():
    return {"message": "AI Voice Caller is running"}
