"""Classification Agent - classifies requests into categories."""
import logging
import re

logger = logging.getLogger(__name__)

AGENT_NAME = "ClassificationAgent"

CATEGORY_KEYWORDS = {
    "Hostel": ["hostel", "room", "dormitory", "accommodation", "bed", "mess", "canteen"],
    "Maintenance": ["repair", "broken", "fix", "maintenance", "plumbing", "electrical", "water", "cooler", "fan", "ac", "air conditioner"],
    "Facilities": ["facility", "building", "block", "lab", "library", "parking", "garden", "cleaning"],
    "Academics": ["course", "exam", "grade", "professor", "lecture", "assignment", "syllabus", "academic"],
    "Finance": ["fee", "scholarship", "payment", "refund", "financial", "tuition", "invoice"],
    "Administration": ["permission", "event", "certificate", "registration", "enrollment", "letter"],
    "IT Support": ["wifi", "internet", "computer", "software", "network", "email", "password", "it support", "lab equipment"],
    "Lost and Found": ["lost", "found", "missing", "belongings"],
    "Student Grievance": ["complaint", "grievance", "harassment", "discrimination", "unfair"],
}


def run(state: dict) -> dict:
    """Classify the request into a category."""
    title = state.get("title", "")
    description = state.get("description", "")
    text = f"{title} {description}".lower()

    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[category] = score

    if scores:
        category = max(scores, key=scores.get)
    else:
        category = "Other"

    state["category"] = category
    state["current_step"] = "CLASSIFICATION"

    logger.info(f"ClassificationAgent: Request classified as '{category}'")
    return state
