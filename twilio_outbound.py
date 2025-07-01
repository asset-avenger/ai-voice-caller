import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TARGET_PHONE_NUMBER")
twiml_app_url = "https://ai-voice-caller-ptkq.onrender.com/voice"  # Matches new endpoint

print(f"✅ TWILIO_ACCOUNT_SID: {account_sid}")

client = Client(account_sid, auth_token)

call = client.calls.create(
    to=to_number,
    from_=from_number,
    url=twiml_app_url
)

print(f"📞 Outbound call initiated. SID: {call.sid}")
