# Multimodal Construction Intelligence Platform

A full-stack capstone starter project based on the epics shown in your screenshots.

## Features included
- FastAPI backend with validated JSON response schemas
- React + Vite frontend
- Construction image upload interface
- Demo safety/PPE and crack-analysis endpoints (heuristic demo, not a certified inspection system)
- Construction task planning and material/cost estimation
- Simple real-estate valuation calculator
- Construction assistant and weather-aware advisory demo
- Health endpoint and basic error handling

## Requirements
- Python 3.9+
- Node.js 18+
- npm

## 1. Run the backend
From this folder:

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## 2. Run the frontend
Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173).

The frontend calls the backend at http://127.0.0.1:8000.

## 3. AI provider configuration
This starter runs without an API key using transparent demo heuristics. To add a multimodal LLM, set an API key in the backend environment and implement the provider call in `backend/app/services/ai_service.py`. Do not put API keys in React or commit them to GitHub.

## Important limitations
The image-analysis logic is a demonstration scaffold. It does not perform reliable real-world PPE detection or structural crack diagnosis. Use a trained vision model and qualified professional review before making safety or engineering decisions. Cost and valuation results are estimates based on user-entered assumptions.
