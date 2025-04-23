# 🧠 Speech and Sign-to-Text Project

This project combines **Speech-to-Text** and **Sign Language Recognition** using Python, FastAPI, and Machine Learning models. It allows users to upload either an audio file or an image of a hand gesture and get a predicted transcription or sign language label.

---

## 📂 Project Structure

| File / Folder       | Description |
|---------------------|-------------|
| `main.py`           | FastAPI app entry point. Integrates both speech and sign language routes. |
| `sign_language.py`  | Endpoint to process sign language gesture images and return predictions. |
| `transcribe.py`     | Endpoint to transcribe audio files into text using Whisper and FFmpeg. |
| `train_model.py`    | Script used to train the sign language recognition model. |
| `models.py`         | Code for loading, saving, and handling ML models. |
| `utils.py`          | Helper functions for preprocessing, file handling, etc. |
| `index.html`        | Simple frontend (optional) to upload files and interact with the API. |
| `README.md`         | Project overview and setup instructions. |

---

## 🚀 Features

✅ Transcribes speech to text using OpenAI Whisper  
✅ Recognizes hand gestures (sign language) using a trained TensorFlow/Keras model  
✅ Built with FastAPI for performance and simplicity  
✅ Easy API access via `/predict/` and `/transcribe/`  
✅ Model training script included (`train_model.py`)  
✅ Clean code structure and modular design

---

📌 TODO / Future Enhancements
 Add gesture landmarks using MediaPipe or OpenCV

 Add live webcam capture for gesture detection

 Improve accuracy with more training data

 Frontend dashboard to upload audio/images

 Dockerize the app for deployment
