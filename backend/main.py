from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import tensorflow as tf
import numpy as np
import io
import os
from contextlib import asynccontextmanager

# Constants
IMG_SIZE = 28
NUM_CLASSES = 50  # Match with len(class_names)
MODEL_PATH = "doodle.h5"            

# List of class names
class_names = [
    'ambulance', 'belt', 'bear', 'bulldozer', 'blueberry', 'airplane', 'bread', 
    'bat', 'apple', 'bandage', 'beach', 'asparagus', 'blackberry', 'backpack', 
    'baseball', 'book', 'arm', 'alarm clock', 'broccoli', 'beard', 'boomerang', 
    'birthday cake', 'bird', 'bottlecap', 'The Eiffel Tower', 'anvil', 'barn', 
    'banana', 'brain', 'basketball', 'angel', 'ant', 'animal migration', 'axe', 
    'baseball bat', 'bed', 'bee', 'bench', 'bicycle', 'binoculars', 'bowtie', 
    'bracelet', 'bridge', 'broom', 'bucket', 'bus', 'bush', 'butterfly', 'cactus', 'cake'
]

# Global model variable
model = None

def create_model():
    """Create the model architecture to match the training notebook"""
    return tf.keras.Sequential([
        tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1)),
        
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Dropout(0.2),
        
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Dropout(0.3),
        
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Dropout(0.4),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        
        tf.keras.layers.Dense(len(class_names), activation='softmax')
    ])

def load_model():
    """Load the model and weights"""
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        print("Creating model architecture...")
        model = create_model()
        
        print("Compiling model...")
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"Loading weights from {MODEL_PATH}...")
        model.load_weights(MODEL_PATH)
        
        print("Model loaded successfully")
        # Print model summary for verification
        model.summary()
        return True
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        model = None
        return False

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((IMG_SIZE, IMG_SIZE))  # Resize
    img_array = np.array(image, dtype=np.float32)
    img_array = img_array / 255.0  # Normalize
    return img_array.reshape((1, IMG_SIZE, IMG_SIZE, 1))

def get_top_predictions(predictions: np.ndarray, k: int = 5):
    """Get top k predictions with their confidences"""
    probabilities = tf.nn.softmax(predictions).numpy()[0]
    top_indices = np.argsort(probabilities)[-k:][::-1]
    
    return [{
        "class": class_names[idx],
        "confidence": round(float(probabilities[idx]) * 100, 2)
    } for idx in top_indices]

# Add this import at the top with other imports
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for model loading and cleanup"""
    # Load model on startup
    try:
        load_model()
        yield
    finally:
        # Cleanup on shutdown
        global model
        model = None

app = FastAPI(
    title="Doodle Recognition API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Doodle Recognition API is running"}

@app.post("/predict/")
async def predict_doodle(file: UploadFile = File(...)):
    # Validate model status
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model(processed_image, training=False)
        top5_results = get_top_predictions(predictions)
        
        # Return results
        return {
            "prediction": top5_results[0]["class"],
            "confidence": top5_results[0]["confidence"],
            "top_5": top5_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)