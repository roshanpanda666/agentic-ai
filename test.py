from TTS.api import TTS
import sounddevice as sd
import numpy as np

# 🎙️ Load the model
print("Initiating voice engine...")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# 🔉 Generate speech waveform directly
text = "Hello Roshan, this is Coqui speaking LIVE!"
wav = tts.tts(text)

# 📢 Play the audio using sounddevice
sd.play(np.array(wav), samplerate=22050)
sd.wait()  
