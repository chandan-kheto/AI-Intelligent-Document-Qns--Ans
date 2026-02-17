
import pyttsx3, pythoncom

class TextToSpeech:
    def __init__(self, rate=170):
        self.rate = rate


    def speak(self, text: str):
        if not text: return

        try:
            pythoncom.CoInitialize()

            engine = pyttsx3.init(driverName="sapi5")
            engine.setProperty("rate", self.rate)

            voices = engine.getProperty("voices")
            if voices:
              engine.setProperty(
                "voice",
                 voices[1].id if len(voices) > 1 else voices[0].id
            )

            engine.say(str(text))
            engine.runAndWait()
            engine.stop()

        except Exception as e:
           print(f"TTS Error: {e}")


