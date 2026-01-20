import librosa
import numpy as np

def analyze_voice(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=16000)

        rms = float(np.mean(librosa.feature.rms(y=y)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        stress = min(1.0, (rms * 3 + zcr * 2))
        return float(stress)

    except Exception:
        return None
