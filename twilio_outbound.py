# twilio_outbound.py
import os
from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TARGET_PHONE_NUMBER")
websocket_url = "wss://your-app.onrender.com/stream"

client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml=f'''
    <Response>
        <Start>
            <Stream url="{websocket_url}" />
        </Start>
        <Say>Hello, this is your AI assistant calling about your property. How can I help you today?</Say>
    </Response>
    ''',
    to=to_number,
    from_=from_number
)

print(f"📞 Call initiated. SID: {call.sid}")
