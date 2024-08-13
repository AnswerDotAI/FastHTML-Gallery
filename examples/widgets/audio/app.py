import base64
from fasthtml.common import *

app, rt = fast_app()
    
@app.get('/')
def homepage():
    audio_path = "African Fella - Cumbia Deli (short).mp3"
    return Titled(audio_path,
                  Div(
                      Audio(src=f"data:audio/mp4;base64,{load_audio_base64(audio_path=audio_path)}", controls=True, id="audio-element"),
                  ))

def load_audio_base64(audio_path: str):
    """ Convert audio file to base64. """
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('ascii')
