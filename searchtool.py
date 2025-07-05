import requests
from bs4 import BeautifulSoup
from TTS.api import TTS
import sounddevice as sd
import numpy as np
import urllib.parse

# 🎙️ Init TTS
print("🔊 Initializing voice engine...")
tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False)
speed = 1.3

def speak(text):
    try:
        print(f"🎤 Speaking: {text}")
        wav = tts.tts(text, speed=speed)
        sd.play(np.array(wav), samplerate=22050)
        sd.wait()
    except Exception as e:
        print("❌ Voice playback failed:", e)

# 🔍 Step 1: Convert any natural query into actual Wikipedia title
def search_wikipedia_title(query):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "format": "json",
        "search": query
    }

    try:
        res = requests.get(search_url, params=params)
        data = res.json()
        if data[1]:
            return data[1][0]  # best matched article title
        else:
            return None
    except Exception as e:
        print(f"❌ Wikipedia search failed: {e}")
        return None

# 🌐 Step 2: Scrape article content from matched Wikipedia title
def fetch_from_wikipedia(title):
    encoded_title = urllib.parse.quote(title.replace(" ", "_"))
    url = f"https://en.wikipedia.org/wiki/{encoded_title}"
    print(f"🌐 Fetching: {url}")

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        # Get the first few paragraphs
        paragraphs = soup.select("p")
        content = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                content.append(text)
            if len(content) >= 3:
                break

        return content, url

    except Exception as e:
        print(f"⚠️ Failed to fetch Wikipedia page: {e}")
        return [], url

# 🚀 Start Assistant Loop
speak("Welcome to your Wikipedia-powered smart AI assistant. Ask me anything!")

while True:
    query = input("\n📝 What do you want to know? ")

    # Convert natural language to Wikipedia page title
    page_title = search_wikipedia_title(query)

    if not page_title:
        speak("Sorry, I couldn't find anything related to that.")
        continue

    print(f"🔎 Matched Wikipedia title: {page_title}")

    results, page_url = fetch_from_wikipedia(page_title)

    if not results:
        speak("Sorry, I couldn't fetch the content.")
        continue

    print(f"\n📄 Reading from: {page_url}")
    for para in results:
        print(f"📝 {para}\n")
        speak(para)
