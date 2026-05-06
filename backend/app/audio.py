# app/audio.py

import whisper

model = whisper.load_model("base")  # small + fast

def transcribe_audio(file_path):
    result = model.transcribe(file_path)

    segments = result["segments"]

    # structure it nicely
    transcript_data = []
    full_text = ""

    for seg in segments:
        transcript_data.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })
        full_text += seg["text"] + " "

    return full_text, transcript_data