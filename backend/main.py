from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import io
import os
import numpy as np
from contextlib import asynccontextmanager

IMG_SIZE = 28
MODEL_PATH = "doodle.pth"

class_names = [
    "axe", "airplane", "apple", "banana", "baseball", "baseball bat", "birthday cake",
    "book", "bucket", "bus", "candle", "camera", "car", "cell phone", "cloud",
    "coffee cup", "crown", "dolphin", "donut", "dumbbell", "envelope", "eye",
    "eyeglasses", "finger", "fish", "flashlight", "flower", "fork", "golf club",
    "hammer", "hand", "headphones", "hot air balloon", "hourglass", "ice cream",
    "key", "knife", "ladder", "leaf", "light bulb", "lightning", "mountain",
    "mushroom", "octagon", "pencil", "pliers", "screwdriver", "see saw", "star",
    "sword", "syringe", "tooth", "toothbrush", "traffic light", "t-shirt", "umbrella",
    "vase", "windmill", "wine glass", "zigzag"
]

class DoodleClassifier(nn.Module):
    def __init__(self, num_classes=60):
        super(DoodleClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)
        self.bn1 = nn.BatchNorm2d(6)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.bn2 = nn.BatchNorm2d(16)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.fc1 = nn.Linear(400, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        x = F.pad(x, (2, 2, 2, 2))
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = x.view(-1, 400)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        model = DoodleClassifier(num_classes=len(class_names)).to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()
        print(f"Model loaded successfully on {device}")
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading model...")
    load_model()
    yield
    print("Shutting down...")

app = FastAPI(title="Doodle Recognition API", lifespan=lifespan)

# List of allowed origins
origins = [
    "http://localhost",              # Allow local dev frontend
    "http://localhost:3000",        # e.g., React dev server
    "https://doodle-classification-system.onrender.com",    # Your production frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)

def predict_image(image: Image.Image):
    """
    Process image to match the notebook implementation:
    - Convert to grayscale
    - Resize to 28x28
    - Invert colors (white on black becomes black on white)
    - Normalize to [0,1]
    """
    # Convert to grayscale
    image = image.convert('L')
    
    # Resize to 28x28
    image = image.resize((IMG_SIZE, IMG_SIZE))
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Invert and normalize to [0,1] as in the notebook
    # In the notebook, you're using black drawings on white background (1-x/255)
    img_array = 1 - (img_array / 255.0)
    
    # Convert to tensor with proper dimensions [1, 1, 28, 28]
    img_tensor = torch.tensor(img_array.reshape(1, 1, 28, 28), dtype=torch.float32).to(device)
    
    # Print debug info about the tensor
    print(f"Tensor shape: {img_tensor.shape}")
    print(f"Tensor min value: {img_tensor.min().item()}, max value: {img_tensor.max().item()}")
    
    # Save normalized image for debugging
    debug_img = (img_array * 255).astype(np.uint8)
    Image.fromarray(debug_img.reshape(28, 28)).save("debug_processed.png")
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = F.softmax(outputs, dim=1)[0]
        top5_values, top5_indices = torch.topk(probabilities, 5)
        
        # Convert tensors to CPU and numpy for processing
        values = top5_values.cpu().numpy()
        indices = top5_indices.cpu().numpy()
        
        # Print debug information
        print("\nPrediction Details:")
        print("-" * 30)
        for val, idx in zip(values, indices):
            print(f"{class_names[idx]:20s}: {val*100:6.2f}%")
        
        # Create predictions list
        predictions = []
        for val, idx in zip(values, indices):
            predictions.append({
                "class": class_names[idx],
                "confidence": round(float(val) * 100, 2)
            })
        
        return predictions

@app.get("/")
async def root():
    return {"message": "Doodle Recognition API is running"}

@app.post("/predict/")
async def predict_doodle(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Save original image for debugging
        image.save("debug_original.png")
        
        # Get predictions
        predictions = predict_image(image)
        
        return {
            "prediction": predictions[0]["class"],
            "confidence": predictions[0]["confidence"],
            "top_5": predictions
        }
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)