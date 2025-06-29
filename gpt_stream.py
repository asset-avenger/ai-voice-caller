# gpt_stream.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def stream_gpt_response(transcript):
    prompt = f'''
You are an AI outbound agent for a company that helps homeowners recover excess proceeds after foreclosure.
The person on the call just said: "{transcript}"
Respond concisely and persuasively. Anticipate objections like:
- "How did you get my number?"
- "I'm not interested."
- "Is this a scam?"
Use simple, human language. Avoid sounding like a robot. Speak as if you're on the phone.
'''
    client = openai.AsyncOpenAI()

    stream = await client.chat.completions.create(
        model="gpt-4o",
        stream=True,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a persuasive, trustworthy AI voice agent."},
            {"role": "user", "content": prompt}
        ],
    )

    async for chunk in stream:
        if hasattr(chunk.choices[0].delta, "content"):
            yield chunk.choices[0].delta.content
