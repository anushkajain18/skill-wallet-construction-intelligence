from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class HealthResponse(BaseModel):
    status: str
    message: str

class Finding(BaseModel):
    title: str
    severity: Literal["low", "medium", "high", "unknown"]
    description: str
    recommended_action: str

class AnalysisResponse(BaseModel):
    analysis_type: str
    image_name: str = "uploaded image"
    summary: str
    findings: List[Finding]
    confidence_note: str
    disclaimer: str

class PlanningRequest(BaseModel):
    project_name: str = Field(default="Sample Construction Project", min_length=1, max_length=120)
    built_up_area_sqft: float = Field(gt=0, le=10000000)
    floors: int = Field(default=1, ge=1, le=100)
    cost_per_sqft: float = Field(default=1800, gt=0, le=100000)
    contingency_percent: float = Field(default=10, ge=0, le=50)
    start_date: Optional[str] = None

class PlanTask(BaseModel):
    task: str
    duration_days: int
    depends_on: List[str] = []

class PlanningResponse(BaseModel):
    project_name: str
    estimated_duration_days: int
    estimated_base_cost: float
    contingency_amount: float
    estimated_total_cost: float
    approximate_materials: dict
    schedule: List[PlanTask]
    assumptions: List[str]

class ValuationRequest(BaseModel):
    location: str = Field(default="Not specified", max_length=120)
    area_sqft: float = Field(gt=0, le=10000000)
    rate_per_sqft: float = Field(gt=0, le=10000000)
    building_age_years: int = Field(default=0, ge=0, le=200)
    depreciation_percent_per_year: float = Field(default=1, ge=0, le=10)

class ValuationResponse(BaseModel):
    location: str
    area_sqft: float
    gross_value: float
    depreciation_percent: float
    estimated_value: float
    note: str

class AssistantRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    context: Optional[str] = Field(default=None, max_length=3000)

class AssistantResponse(BaseModel):
    answer: str
    suggested_next_steps: List[str]
    disclaimer: str

class WeatherAdvisoryRequest(BaseModel):
    weather: Literal["sunny", "hot", "rainy", "stormy", "windy", "unknown"] = "unknown"
    activity: Literal["concrete_pouring", "roof_work", "painting", "excavation", "general"] = "general"
    temperature_c: Optional[float] = Field(default=None, ge=-30, le=60)

class WeatherAdvisoryResponse(BaseModel):
    weather: str
    activity: str
    risk_level: Literal["low", "medium", "high", "unknown"]
    recommendations: List[str]
    note: str
