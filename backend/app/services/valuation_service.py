from ..schemas import ValuationRequest, ValuationResponse

def estimate_valuation(req: ValuationRequest) -> ValuationResponse:
    gross = req.area_sqft * req.rate_per_sqft
    depreciation = min(req.building_age_years * req.depreciation_percent_per_year, 80)
    value = gross * (1 - depreciation / 100)
    return ValuationResponse(
        location=req.location,
        area_sqft=req.area_sqft,
        gross_value=round(gross, 2),
        depreciation_percent=round(depreciation, 2),
        estimated_value=round(value, 2),
        note="Indicative arithmetic estimate only. It is not a professional appraisal and does not account for legal title, location-specific market factors, condition, or comparable sales."
    )
