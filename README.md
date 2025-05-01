# Doodle Recognition Project
*6th Semester Project - Deep Learning

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

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure
```
doodle/
├── app/                  # Next.js pages
│   └── page.tsx         # Main page
├── backend/             # FastAPI backend
│   ├── main.py         # API endpoints
│   └── doodle.pth      # Model weights
├── components/          # React components
│   └── doodle-canvas.tsx
└── public/             # Static assets
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/predict/` | POST | Submit doodle for recognition |

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

## Future Improvements
- [ ] Add more doodle classes
- [ ] Implement user feedback loop
- [ ] Add undo/redo functionality
- [ ] Export drawings
- [ ] Share predictions on social media

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## About
This project was developed as part of the 6th semester coursework in Computer Science Engineering, focusing on practical applications of deep learning and full-stack development.

## License
This project is part of academic coursework.

## Acknowledgments
- Quick, Draw! Dataset by Google
- PyTorch community
- FastAPI framework
- Next.js team

---

*Built with 💻 and ☕ by CSE Students*