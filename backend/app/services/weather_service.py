from ..schemas import WeatherAdvisoryRequest, WeatherAdvisoryResponse

def create_weather_advisory(req: WeatherAdvisoryRequest) -> WeatherAdvisoryResponse:
    recommendations = []
    risk = "low"
    if req.weather == "stormy":
        risk = "high"
        recommendations += ["Pause exposed outdoor work when lightning or unsafe wind is present.", "Secure loose materials and follow the site's emergency plan."]
    elif req.weather == "rainy":
        risk = "medium"
        recommendations += ["Check excavation stability, slippery access routes, and water accumulation.", "Protect cement and other moisture-sensitive materials."]
    elif req.weather == "windy":
        risk = "medium"
        recommendations += ["Assess lifting operations and work at height against site wind limits.", "Secure sheets, scaffolds, and loose materials."]
    elif req.weather == "hot" or (req.temperature_c is not None and req.temperature_c >= 35):
        risk = "medium"
        recommendations += ["Provide drinking water, shade, rest breaks, and heat-stress monitoring.", "Follow the site's heat-work policy."]
    else:
        recommendations += ["Check the latest local forecast and site-specific work limits before starting."]
    if req.activity == "concrete_pouring" and req.weather in ("rainy", "stormy"):
        recommendations.append("Ask the site engineer whether concrete placement should be delayed or protected.")
        risk = "high" if req.weather == "stormy" else "medium"
    if req.activity == "roof_work" and req.weather in ("windy", "rainy", "stormy"):
        recommendations.append("Stop roof work when surfaces or wind conditions exceed approved safety limits.")
        risk = "high" if req.weather == "stormy" else "medium"
    return WeatherAdvisoryResponse(
        weather=req.weather,
        activity=req.activity,
        risk_level=risk,
        recommendations=recommendations,
        note="Advisory is based only on the inputs entered. It does not fetch live weather or replace the site safety plan."
    )
