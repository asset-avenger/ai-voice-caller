# audio_utils.py
import audioop
from pydub import AudioSegment
import io

def convert_to_mulaw(audio_bytes: bytes) -> bytes:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    audio = audio.set_channels(1).set_frame_rate(8000).set_sample_width(2)
    raw_pcm = audio.raw_data
    return audioop.lin2ulaw(raw_pcm, 2)
