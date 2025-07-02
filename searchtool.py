from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from TTS.api import TTS
import sounddevice as sd
import numpy as np

# Switch to fast_pitch model (supports speed control)
print("🔊 Initializing voice engine...")
tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False)

# Set speaking speed
speed = 2  # >1 = slower, <1 = faster

# Speak function with speed control
def speak(text):
    try:
        print(f"🎤 Speaking: {text}")
        wav = tts.tts(text, speed=speed)
        sd.play(np.array(wav), samplerate=22050)
        sd.wait()
    except Exception as e:
        print("❌ Voice playback failed:", e)

# Intro message
speak("Welcome to your AI search assistant. Ask me anything!")

# Search loop
while True:
    query = input("\n📝 Enter your query: ")

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=1)
        for r in results:
            title = r['title']
            link = r['href']

            print(f"\n🔗 Title: {title}")
            print(f"🌐 Link: {link}")
            speak(f"Here is what I found: {title}")

            try:
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                res = requests.get(link, headers=headers, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')

                paragraphs = soup.find_all('p')
                print("📝 First few lines:")

                spoken_count = 0
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        print(f" - {text}")
                        speak(text)
                        spoken_count += 1
                    if spoken_count >= 3:
                        break

            except Exception as e:
                print(f"⚠️ Could not scrape {link}: {e}")
                speak("Sorry, I couldn't fetch the content from that page.")
