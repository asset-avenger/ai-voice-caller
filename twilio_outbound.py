import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
recipient_number = os.getenv("RECIPIENT_PHONE_NUMBER")
render_stream_url = os.getenv("RENDER_STREAM_URL")

client = Client(account_sid, auth_token)

call = client.calls.create(
    to=recipient_number,
    from_=twilio_number,
    twiml=f"""
        <Response>
            <Start>
                <Stream url="{render_stream_url}" />
            </Start>
            <Say voice="Polly.Joanna">Connecting you to a representative...</Say>
        </Response>
    """
)

print(f"📞 Call initiated. SID: {call.sid}")
