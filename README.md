<div align="center">
  <img src="logo.png" alt="logo">
</div>

Greetings fellow future-gadget lab members, this is the documentation for my side project, called Amadeus, as the name implies this application aims to recreate or at least give life to Amadeus from steins;gate 0

additionally, this application is made specifically for desktops and aims to recreate Amadeus as shown in the Viktor chondria university (see episode 2 of steins;gate 0 for context)

please keep in mind that this project is still a work in progress and that im just an enthusiastic fan of steins;gate franchise, furthermore im still newbie when it comes to programming as such expect a lot of limitaions from the application

I did my best to make it as anime-accurate as possible, with that said below contains the steps on how to properly install the app in your desktop and other technical information about the app

el psy kongroo -

### 🖥️ Installation
**Option 1: clone the repository and bundle the app yourself**

**Step 1:** clone the repository
git https://github.com/senkuuuuu/-proj.-10-Amadeus.git

**Step 2:** Install dependencies, you can make a virtual environment if you want to
```
pip install -r requirements.txt
```
or
```
pip install pygame-ce==2.5.5 pygame_gui==0.6.14 yaudio soundfile numpy sounddevice python-dotenv SpeechRecognition transformers torch git+https://github.com/Xtr4F/PyCharacterAI.git@5629da4820bcd15bbb991cf0e5cd23f54d106cdd
```

**Step 3:** create an account in unrealspeech then obtain your own auth key
https://unrealspeech.com/

**Step 4:** find your own character ai token/key. go to the link below to find how:
https://github.com/Xtr4F/PyCharacterAI

**Step 5:** create your own .env file then add the following:
```
CHARACTER_AI_TOKEN = "your character ai token"
UNREAL_VOICE_AUTHORIZATION_KEY = "your unreal voice auth key"
```

**Step 6:** use pyinstaller to bundle the codebase
```
pyinstaller --onefile --name=Amadeus --icon=logo.ico --add-data "resources;resources" --windowed main.py
```

**Option 2: Install the readily available bundled version of the application _(COMING SOON)_**
Currently, the app relies on API keys (for CharacterAI and UnrealSpeech), but I plan to remove this requirement in the future so that less technically inclined fans can still enjoy a desktop version of our beloved Amadeus


---

### ⭐ Features
| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| **Log-in system**            | Uses a file-based database controlled by the main app via SQLite.           |
| **Seamless GUI design**      | Achieved through a combination of `asyncio`, `pygame`, and `pygame_gui`.    |
| **Voice input**              | Implemented using `PyAudio`, `wave`, and `SpeechRecognition` modules.       |
| **Expressive character animation** | Powered by emotion analysis using a custom-trained DistilBERT model (trained on 3,000+ data points). |
| **Lore-accurate responses**   | Enabled by integrating Character AI with the main app using `PyCharacterAI`. |

---

### ⛓️ Limitations
- fixed window size
- large download size (because of NLP Models)
---


## 📝 To do
- make window size flexible
- clone voice of makise kurisu
- further train the model for emotion analysis
- exchange characterai with well trained GPT
---

## 🎁 Support
support the development of our beloved amadeus, any form of support is welcomed, whether through code contributions or financial donations

ko-fi: https://ko-fi.com/makisekurisu22217 

