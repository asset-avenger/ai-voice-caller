# twilio_outbound.py
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials and phone numbers
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("CALL_TARGET_NUMBER")

# Create Twilio client
client = Client(account_sid, auth_token)

# Set up TwiML to connect call to your WebSocket server
twiml = VoiceResponse()
twiml.connect().stream(url="wss://ai-voice-caller-ptkq.onrender.com/stream")

# Make the call
call = client.calls.create(
    twiml=str(twiml),
    to=to_number,
    from_=from_number
)

print(f"📞 Outbound call initiated. Call SID: {call.sid}")
