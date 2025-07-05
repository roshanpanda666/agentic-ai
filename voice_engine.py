import numpy as np
import sounddevice as sd
from TTS.api import TTS

print("🔊 Initializing TTS Engine...")

# 🚀 Load the TTS model once
tts_model = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False)
default_speed = 1.3

# 🎙️ Speak Function
def speak(text, speed=default_speed):
    try:
        print(f"🎤 Speaking: {text}")
        wav = tts_model.tts(text, speed=speed)
        sd.play(np.array(wav), samplerate=22050)
        sd.wait()
    except Exception as e:
        print("❌ Voice playback failed:", e)
