from elevenlabs import generate, save, set_api_key
from playsound import playsound
import uuid
import os

set_api_key("sk_3c17d05bf0c110f6dc490d2f74ac951feb4a8c9f469a11ed")

def speak(text):
    try:
        audio = generate(
            text=text,
            voice="Aria",  # Or your voice ID
            model="eleven_multilingual_v2"
        )
        # Save to a temp file
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        save(audio, filename)
        playsound(filename)
        os.remove(filename)  # Optional: clean up
    except Exception as e:
        print("❌ Voice generation failed:", e)
