import speech_recognition as sr
import numpy as np

def process_audio(audio_data):
    """
    Verarbeitet die aufgenommenen Audiodaten, verstärkt sie und gibt sie für die Spracherkennung zurück.
    """
    # Rohdaten aus der AudioData extrahieren
    raw_audio = audio_data.get_wav_data()

    # PCM-Daten extrahieren und als numpy-Array interpretieren
    sample_rate = audio_data.sample_rate
    sample_width = audio_data.sample_width  # Bytes pro Sample
    print(f"samle rate {sample_rate}")
    print(f"sample width {sample_width}")

    # Konvertiere Rohdaten in ein numpy-Array
    dtype = np.int32 if sample_width == 2 else np.int8
    audio_array = np.frombuffer(raw_audio, dtype=dtype)

    # Verstärke das Audiosignal (z.B. um den Faktor 3)
    amplified_audio_array = np.clip(audio_array * 1, np.iinfo(dtype).min, np.iinfo(dtype).max)

    # Konvertiere das verstärkte numpy-Array zurück zu Bytes
    amplified_audio_bytes = amplified_audio_array.astype(dtype).tobytes()

    # Verstärktes Audio in ein AudioData-Objekt umwandeln
    return sr.AudioData(amplified_audio_bytes, sample_rate, sample_width)
