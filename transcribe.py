import whisper
import mysql.connector
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# ✅ Load model only once
model = whisper.load_model("base")

def transcribe_audio(audio_path, user_choice="auto"):
    # Transcription logic
    if user_choice.lower() == 'auto':
        result = model.transcribe(audio_path, task='transcribe')
    else:
        result = model.transcribe(audio_path, task='transcribe', language=user_choice, fp16=False,
                                  suppress_tokens=list(range(50258, 50267)))

    transcription_text = result['text']
    detected_language = result['language']
    file_name = audio_path.split('/')[-1]

    return transcription_text, detected_language, file_name


def save_transcription_to_db(file_name, text, language):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu!TheGr8",
        database="speech_to_text"
    )
    cursor = conn.cursor()
    query = "INSERT INTO transcriptions (file_name, transcription, language) VALUES (%s, %s, %s)"
    cursor.execute(query, (file_name, text, language))
    conn.commit()
    cursor.close()
    conn.close()
