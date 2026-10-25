from pathlib import Path
from ..schemas import AnalysisResponse, Finding

def analyze_construction_image(content: bytes, analysis_type: str = "both") -> AnalysisResponse:
    # Demo-only placeholder: it validates the image but does not run a vision model.
    findings = []
    normalized = analysis_type.lower()
    if normalized in ("safety", "both"):
        findings.append(Finding(
            title="PPE / site-safety review required",
            severity="unknown",
            description="The starter does not yet detect helmets, vests, barriers, or other PPE from pixels.",
            recommended_action="Review the image manually, or connect a validated object-detection model and define its confidence threshold."
        ))
    if normalized in ("crack", "both"):
        findings.append(Finding(
            title="Structural crack review required",
            severity="unknown",
            description="The starter does not diagnose crack type or severity from the uploaded image.",
            recommended_action="Have a qualified structural professional inspect the location and measure crack width, pattern, and progression."
        ))
    if not findings:
        findings.append(Finding(
            title="Analysis type not recognized",
            severity="low",
            description="Choose safety, crack, or both for the analysis type.",
            recommended_action="Run the analysis again using one of the supported options."
        ))
    return AnalysisResponse(
        analysis_type=analysis_type,
        summary="Image received and validated. This MVP returns a review checklist rather than claiming automated detection.",
        findings=findings,
        confidence_note="No computer-vision model is connected in this starter, so no detection confidence score is available.",
        disclaimer="Do not use this demo as a substitute for a site safety inspection or structural engineering assessment."
    )
