# AI Voice Caller

This project is a low-latency, intelligent outbound AI voice caller stack powered by:

- 🧠 OpenAI (GPT-4o) for real-time conversation
- 🔊 ElevenLabs for high-quality speech synthesis
- 🗣️ Google Cloud Speech-to-Text for transcription
- ☎️ Twilio for outbound calls and audio streaming
- 🛠️ Deployed via Render using FastAPI + WebSockets

## Deploy Instructions

1. Fork this repo into your GitHub account
2. Go to [Render.com](https://render.com), create a new **Web Service**
3. Link to your GitHub repo
4. Use this Start Command:

```
uvicorn main:app --host 0.0.0.0 --port 10000
```

5. Set all variables from `.env.template` into Render’s dashboard

You'll receive a public WebSocket URL like:

```
wss://your-app.onrender.com/stream
```

Use this in your Twilio call XML stream URL.
