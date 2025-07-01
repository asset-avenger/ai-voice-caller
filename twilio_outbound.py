import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
render_ws_url = os.getenv("RENDER_STREAM_URL")

# Get phone number from CLI or fallback to .env
if len(sys.argv) >= 2:
    target_number = sys.argv[1]
else:
    target_number = os.getenv("TARGET_PHONE_NUMBER")

if not target_number:
    print("❌ ERROR: No phone number provided in CLI or .env")
    sys.exit(1)

client = Client(account_sid, auth_token)

print(f"✅ Dialing {target_number} from {twilio_number}")

call = client.calls.create(
    twiml=f'<Response><Start><Stream url="{render_ws_url}" /></Start><Say>Connecting you now.</Say></Response>',
    to=target_number,
    from_=twilio_number
)

print(f"📞 Call initiated. SID: {call.sid}")
