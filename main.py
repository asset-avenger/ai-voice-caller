import os
import json
import asyncio
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Stream
from typing import Dict, Any
import websockets

load_dotenv()

app = FastAPI()
STREAM_URL = os.getenv("RENDER_STREAM_URL")  # WebSocket URL for ElevenLabs agent
ELEVENLABS_WS_URL = os.getenv("ELEVENLABS_WS_URL")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.post("/voice")
async def voice_handler(request: Request):
    vr = VoiceResponse()
    vr.append(Stream(url=STREAM_URL))
    return PlainTextResponse(content=str(vr), media_type="text/xml")

@app.websocket("/stream")
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:
        eleven_ws = await connect_to_elevenlabs()

        async def twilio_to_eleven():
            while True:
                msg = await ws.receive_text()
                data = json.loads(msg)
                if data.get("event") == "media":
                    audio_payload = data["media"]["payload"]
                    await eleven_ws.send(audio_payload)
                elif data.get("event") == "stop":
                    await eleven_ws.send("EOS")
                    break

        async def eleven_to_twilio():
            while True:
                chunk = await eleven_ws.recv()
                frame = json.dumps({"event": "media", "media": {"payload": chunk}})
                await ws.send_text(frame)

        await asyncio.gather(twilio_to_eleven(), eleven_to_twilio())

    except WebSocketDisconnect:
        print("🔌 Client disconnected")
    finally:
        await ws.close()

async def connect_to_elevenlabs():
    headers = {
        "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
    }
    return await websockets.connect(ELEVENLABS_WS_URL, extra_headers=headers)

@app.get("/")
async def root():
    return {"message": "AI Voice Caller is live with ElevenLabs integration."}
