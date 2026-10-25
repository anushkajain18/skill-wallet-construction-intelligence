from ..schemas import PlanningRequest, PlanningResponse, PlanTask

def build_plan(req: PlanningRequest) -> PlanningResponse:
    area = req.built_up_area_sqft
    base = area * req.cost_per_sqft * req.floors
    contingency = base * req.contingency_percent / 100
    # Transparent illustrative factors only; revise using local specifications and BOQ.
    schedule = [
        PlanTask(task="Site survey and preparation", duration_days=5, depends_on=[]),
        PlanTask(task="Foundation and substructure", duration_days=15, depends_on=["Site survey and preparation"]),
        PlanTask(task="Structure and framing", duration_days=max(15, req.floors * 12), depends_on=["Foundation and substructure"]),
        PlanTask(task="Electrical and plumbing rough-in", duration_days=max(8, req.floors * 5), depends_on=["Structure and framing"]),
        PlanTask(task="Finishing and inspection", duration_days=max(12, req.floors * 7), depends_on=["Electrical and plumbing rough-in"]),
    ]
    duration = sum(t.duration_days for t in schedule)
    materials = {
        "cement_bags_approx": round(area * req.floors * 0.4),
        "steel_kg_approx": round(area * req.floors * 3.5),
        "sand_cubic_ft_approx": round(area * req.floors * 1.2),
        "brick_units_approx": round(area * req.floors * 8)
    }
    return PlanningResponse(
        project_name=req.project_name,
        estimated_duration_days=duration,
        estimated_base_cost=round(base, 2),
        contingency_amount=round(contingency, 2),
        estimated_total_cost=round(base + contingency, 2),
        approximate_materials=materials,
        schedule=schedule,
        assumptions=[
            "All rates and material factors are illustrative placeholders, not a bill of quantities.",
            "The cost formula multiplies area by cost per square foot and number of floors; adjust the input to match how your area is measured.",
            "Actual duration depends on design, approvals, workforce, site conditions, and weather."
        ]
    )
