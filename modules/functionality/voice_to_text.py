import time
import os
import speech_recognition as sr
from queue import Queue

#this dosen't work for python 3.13+
class VoiceToText:
    def __init__(self) -> None:
        self.result_queue = Queue()
    
    def begin(self) -> None:
        try:
            time.sleep(0.2)
            # Initialize the recognizer
            recognizer = sr.Recognizer()

            # Open the audio file
            with sr.AudioFile("temp_input.wav") as source:
                # Record the audio data
                audio_data = recognizer.record(source)

                # Recognize speech using Google Speech Recognition
                text = recognizer.recognize_google(audio_data)
            
            os.remove("temp_input.wav")
            
            return text
        except Exception as e:
            print(e)
            return '...'
    