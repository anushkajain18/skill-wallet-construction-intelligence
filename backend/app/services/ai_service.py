def answer_construction_question(question: str, context: str | None = None) -> dict:
    q = question.lower()
    if any(word in q for word in ["crack", "structural", "column", "beam"]):
        answer = ("Cracks in structural elements should be documented and assessed by a qualified structural engineer. "
                  "Record the location, width, length, pattern, and whether the crack is changing. Do not rely on a photo-only automated diagnosis.")
        steps = ["Keep people away from visibly unstable areas.", "Photograph and measure the crack if safe.", "Arrange a qualified site inspection."]
    elif any(word in q for word in ["helmet", "ppe", "safety", "vest"]):
        answer = ("Use the site's approved safety checklist and verify appropriate PPE, edge protection, signage, access routes, and housekeeping. "
                  "This assistant cannot certify that a site is safe.")
        steps = ["Follow the site safety plan.", "Escalate hazards to the site supervisor.", "Record the observation and corrective action."]
    elif any(word in q for word in ["cost", "budget", "estimate", "material"]):
        answer = ("Start with measured quantities, local supplier rates, labour, equipment, taxes, and a contingency allowance. "
                  "The planning calculator provides a rough placeholder estimate only.")
        steps = ["Prepare a bill of quantities.", "Use current local rates.", "Have a qualified estimator review the budget."]
    else:
        answer = ("For a construction decision, collect the project context, drawings, measurements, site conditions, and applicable local requirements. "
                  "I can provide general guidance, but this demo is not a substitute for a qualified professional.")
        steps = ["Describe the site and activity.", "Include measurements and relevant constraints.", "Verify recommendations with the responsible professional."]
    if context:
        answer += f" Context supplied: {context[:350]}"
    return {
        "answer": answer,
        "suggested_next_steps": steps,
        "disclaimer": "Demo rule-based assistant; no external LLM or live project database is connected."
    }
