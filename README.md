# Doodle Recognition Project
*6th Semester Project - Deep Learning*

![Doodle Recognition Interface](./public/Screenshot%202025-05-01%20063411.png)
![Prediction Results](./public/Screenshot%202025-05-01%20063623.png)
![Drawing Canvas](./public/Screenshot%202025-05-01%20063554.png)

## Overview
This project implements a real-time doodle recognition system that can identify hand-drawn sketches. Built with Next.js and FastAPI, it provides an intuitive drawing interface and instant predictions using a deep learning model.

## Live Demo
Visit [http://localhost:3000](http://localhost:3000) to try the application.

## Features
- ✏️ Real-time doodle recognition
- 🎨 Interactive drawing canvas
- 🎯 Top 5 prediction results
- 📱 Mobile-friendly touch support
- ⚡ Instant predictions
- 🔄 Clear canvas option
- 💾 Save drawings locally
- 📊 Confidence score visualization

## Tech Stack

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn UI** - Component library
- **Canvas API** - Drawing interface

### Backend
- **FastAPI** - API framework
- **PyTorch** - Deep learning
- **PIL** - Image processing
- **NumPy** - Numerical computing
- **CORS** - Cross-origin resource sharing

## Model Architecture
- Input: 28x28 grayscale images
- 2 Convolutional layers with batch normalization
- Max pooling layers
- 3 Fully connected layers
- Output: 60 class probabilities

## Supported Classes
The model can recognize 60 different doodles including:
- Common objects (apple, book, car)
- Animals (dolphin, fish)
- Tools (hammer, screwdriver)
- And many more!

Full list of supported classes:

axe, airplane, apple, banana, baseball, baseball bat, birthday cake, book, bucket, bus, candle, camera, car, cell phone, cloud, coffee cup, crown, dolphin, donut, dumbbell, envelope, eye, eyeglasses, finger, fish, flashlight, flower, fork, golf club, hammer, hand, headphones, hot air balloon, hourglass, ice cream, key, knife, ladder, leaf, light bulb, lightning, mountain, mushroom, octagon, pencil, pliers, screwdriver, see saw, star, sword, syringe, tooth, toothbrush, traffic light, t-shirt, umbrella, vase, windmill, wine glass, zigzag


## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- CUDA-capable GPU (optional)

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload
```

### Frontend Setup
```bash
# Navigate to project root
cd doodle-recognition-project

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure
```
└── doodle-recognition-project/
 ├── README.md
 ├── app/
 │ ├── globals.css
 │ ├── layout.tsx
 │ └── page.tsx
 ├── backend/
 │ ├── doodle.pth
 │ ├── doodle_recognition.ipynb
 │ ├── main.py
 │ └── requirements.txt
 ├── components/
 │ ├── doodle-canvas.tsx
 │ └── ui/
 │   ├── badge.tsx
 │   ├── button.tsx
 │   ├── card.tsx
 │   └── slider.tsx
 ├── lib/
 │ └── utils.ts
 ├── public/
 │ ├── images/
 │ └── favicon.ico
 ├── styles/
 │ └── globals.css
 ├── .env.local
 ├── .gitignore
 ├── next.config.js
 ├── package.json
 └── tsconfig.json
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/predict/` | POST | Submit doodle for recognition |

## 🌍 Environment Configuration
This project uses environment variables to configure backend API endpoints and runtime settings.

### 🔧 Setup `.env.local`
Create a `.env.local` file in the root of your project and add the following:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/predict/
ENVIRONMENT=TEST
```

## Development
1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. In a new terminal, start the frontend:
```bash
npm run dev
```

3. Visit [http://localhost:3000](http://localhost:3000)

## How It Works
1. Draw a doodle on the canvas
2. The application captures the drawing as a 28x28 grayscale image
3. The image is sent to the backend API
4. Our trained model analyzes the image and returns predictions
5. The top 5 predictions are displayed with confidence scores

## Performance Optimization
- Canvas drawing is optimized for smooth performance
- Batch prediction to reduce API calls
- Lazy loading for non-critical components
- Model quantization for faster inference

## Troubleshooting

### Common Issues
- **API Connection Error**: Ensure backend server is running on port 8000
- **Blank Canvas**: Try clearing cache and refreshing
- **Slow Predictions**: Check GPU availability and CUDA installation

### Browser Compatibility
Tested and working on:
- Chrome 96+
- Firefox 94+
- Safari 15+
- Edge 96+

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## Future Improvements
- Add more classes to the recognition model
- Implement user accounts to save drawings
- Add social sharing functionality
- Create a gallery of user submissions
- Train model on custom datasets

## About
This project was developed as part of the 8th semester Term Project in Computer Science Engineering, focusing on practical applications of deep learning and full-stack development.

## License
This project is part of academic coursework and is available under the MIT License.

## Acknowledgments
- Quick, Draw! Dataset by Google
- PyTorch community
- FastAPI framework
- Next.js team
- Our course instructors for guidance and support

---
*Built with 💻 and ☕ by [Divyanshu](https://github.com/Divyanshu4fx)*

[Deployment Link](https://doodle-classification-system.vercel.app/)

*Last Updated: May 2025*
