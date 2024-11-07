import base64, requests
from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    audio_path = "https://ucarecdn.com/abb35276-b3cb-4a5c-bba0-878f264e5976/AfricanFellaCumbiaDelishort.mp3"
    return Audio(src=f"data:audio/mp4;base64,{load_audio_base64(audio_path)}", controls=True)

def load_audio_base64(audio_path: str):
    """ Convert audio file to base64. """
    response = requests.get(audio_path)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('ascii')
