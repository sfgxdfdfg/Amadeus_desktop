import pyaudio
import wave
import asyncio

class StartRecording:
    def __init__(self, is_recording:bool, stop_event:asyncio.Event) -> None:
        #metadata
        self.sample_rate = 44100
        self.format = pyaudio.paInt16
        self.channels = 1
        self.chunk = 1024
        self.filename = 'temp_input.wav'

        #flags
        self.is_recording = is_recording
        self.stop_event = stop_event

    def begin(self) -> None:
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)

        print("[DEBUG] Recording...")
        frames = []

        try:
            while self.is_recording and not self.stop_event.is_set():
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
        except Exception as e:
            print(f"[DEBUG] Error during recording: {e}")
        finally:
            # Cleanup resources
            stream.stop_stream()
            stream.close()
            audio.terminate()

            print("[DEBUG] Finished recording.")
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            