from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4

from .schemas import (
    HealthResponse, AnalysisResponse, PlanningRequest, PlanningResponse,
    ValuationRequest, ValuationResponse, AssistantRequest, AssistantResponse,
    WeatherAdvisoryRequest, WeatherAdvisoryResponse
)
from .services.image_service import analyze_construction_image
from .services.planning_service import build_plan
from .services.valuation_service import estimate_valuation
from .services.ai_service import answer_construction_question
from .services.weather_service import create_weather_advisory

app = FastAPI(
    title="Multimodal Construction Intelligence Platform",
    version="1.0.0",
    description="Capstone MVP for construction image analysis, planning, valuation and advisory."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_IMAGE_BYTES = 10 * 1024 * 1024

@app.get("/", response_model=HealthResponse)
def home():
    return HealthResponse(status="running", message="Construction Intelligence API is ready.")

@app.get("/api/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="healthy", message="API and routes are available.")

@app.post("/api/analyze-image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...), analysis_type: str = "both"):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")
    try:
        from PIL import Image
        import io
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        raise HTTPException(status_code=400, detail="The file could not be read as a valid image.")

    # Keep a uniquely named local copy for demo traceability.
    suffix = Path(file.filename or "upload.jpg").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        suffix = ".jpg"
    saved = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    saved.write_bytes(content)
    return analyze_construction_image(content, analysis_type)

@app.post("/api/planning", response_model=PlanningResponse)
def planning(request: PlanningRequest):
    return build_plan(request)

@app.post("/api/valuation", response_model=ValuationResponse)
def valuation(request: ValuationRequest):
    return estimate_valuation(request)

@app.post("/api/assistant", response_model=AssistantResponse)
def assistant(request: AssistantRequest):
    return answer_construction_question(request.question, request.context)

@app.post("/api/weather-advisory", response_model=WeatherAdvisoryResponse)
def weather_advisory(request: WeatherAdvisoryRequest):
    return create_weather_advisory(request)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    # Avoid leaking stack traces to the client in this starter.
    return JSONResponse(status_code=500, content={"detail": "Unexpected server error. Check backend terminal logs."})
