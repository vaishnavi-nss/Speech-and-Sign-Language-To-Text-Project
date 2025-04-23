#online transcription using Fast API
from utils import transcribe_audio, save_transcription_to_db
from models import SessionLocal, Transcription
from fastapi import FastAPI, File, UploadFile, Form
from models import init_db

init_db()

import tempfile
import subprocess
import os

app = FastAPI()

# -------------------------------
# Root route for testing
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# -------------------------------
# Transcription Route
# -------------------------------
@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...), language: str = Form("auto")):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(file.file.read())
            temp_audio_path = temp_audio.name

        # Convert audio to a format supported by Whisper using FFmpeg
        processed_audio_path = temp_audio_path.replace(".wav", ".mp3")
        ffmpeg_command = [
            "ffmpeg", "-i", temp_audio_path,
            "-ar", "16000", "-ac", "1",
            "-c:a", "libmp3lame", processed_audio_path
        ]

        print(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")
        subprocess.run(ffmpeg_command, check=True)

        # Run transcription from utils.py
        text, detected_language, file_name = transcribe_audio(processed_audio_path, language)

        # Save results to database
        save_transcription_to_db(file_name, text, detected_language)

        # Cleanup
        os.remove(temp_audio_path)
        os.remove(processed_audio_path)

        return {
            "file_name": file_name,
            "transcription": text,
            "detected_language": detected_language
        }

    except subprocess.CalledProcessError as ffmpeg_error:
        return {"error": f"FFmpeg error: {ffmpeg_error}"}
    except Exception as e:
        return {"error": str(e)}
