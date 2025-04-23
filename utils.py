import whisper
import mysql.connector
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)

# ✅ Load model only once
try:
    model = whisper.load_model("base")
except Exception as e:
    raise RuntimeError(f"Failed to load Whisper model: {e}")

def transcribe_audio(audio_path, user_choice="auto"):
    """
    Transcribes audio from the given path using Whisper.
    Supports auto language detection or user-specified language.
    Returns transcription text, detected language, and file name.
    """
    try:
        if user_choice.lower() == 'auto':
            result = model.transcribe(audio_path, task='transcribe')
        else:
            result = model.transcribe(
                audio_path,
                task='transcribe',
                language=user_choice,
                fp16=False,
                suppress_tokens=list(range(50258, 50267))
            )

        transcription_text = result['text']
        detected_language = result['language']
        file_name = os.path.basename(audio_path)

        return transcription_text, detected_language, file_name

    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")


def save_transcription_to_db(file_name, text, language):
    """
    Stores the transcription details in a MySQL database.
    Make sure your 'speech_to_text' database and 'transcriptions' table exist.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vaishu!TheGr8",
            database="speech_to_text"
        )
        cursor = conn.cursor()

        query = """
        INSERT INTO transcriptions (file_name, transcription, language)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (file_name, text, language))
        conn.commit()

    except mysql.connector.Error as db_err:
        raise RuntimeError(f"Database error: {db_err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
