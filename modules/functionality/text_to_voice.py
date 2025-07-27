import requests
from dotenv import load_dotenv
import os


# using unreal speech (subject for change)
class TextToVoice:
    def __init__(self, text: str) -> None:
        self.text = text
        load_dotenv()  
    
    def begin(self) -> None:

        # Text to be converted to speech
        inp = self.text

        #conversion using unreal engine voice
        response = requests.post(
            'https://api.v7.unrealspeech.com/stream',
            headers = {
                'Authorization' : os.getenv("UNREAL_VOICE_AUTHORIZATION_KEY")
            },
            json = {
                'Text': f'''{self.text}''', 
                'VoiceId': 'Liv', 
                'Bitrate': '192k', 
                'Speed': '0.05',
                'Pitch': '1.04', 
                'Codec': 'libmp3lame',
            }
        )


        with open('temp_output.mp3', 'wb') as f:
            f.write(response.content)

    
