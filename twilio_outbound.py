# twilio_outbound.py

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load .env file
load_dotenv()

# Get environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TARGET_PHONE_NUMBER")

# Your deployed Render backend URL
websocket_url = "wss://ai-voice-caller-ptkq.onrender.com/stream"

# Create Twilio client
client = Client(account_sid, auth_token)

# Make the call without Twilio <Say> (AI will speak first instead)
call = client.calls.create(
    twiml=f"""
    <Response>
        <Start>
            <Stream url="{websocket_url}" />
        </Start>
    </Response>
    """,
    to=to_number,
    from_=from_number
)

print(f"📞 Call initiated. SID: {call.sid}")
