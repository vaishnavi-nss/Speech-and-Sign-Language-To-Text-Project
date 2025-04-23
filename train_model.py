from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf
import io

# Load model
model = tf.keras.models.load_model('your_sign_language_model.h5')
model.save('your_sign_language_model.h5')


app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image
    img_data = await file.read()
    img = Image.open(io.BytesIO(img_data))
    
    # Preprocess the image (convert to landmarks, etc.)
    landmarks = preprocess_image(img)  # Implement this function based on your model's needs

    # Make a prediction
    prediction = model.predict(np.expand_dims(landmarks, axis=0))
    predicted_label = np.argmax(prediction, axis=1)

    return {"prediction": predicted_label}
