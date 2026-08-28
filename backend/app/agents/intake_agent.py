"""Intake Agent - reads incoming requests and extracts useful information."""
import re
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "IntakeAgent"


def run(state: dict) -> dict:
    """Process intake of a new request."""
    title = state.get("title", "")
    description = state.get("description", "")
    raw_request = f"{title}. {description}" if title else description

    # Extract key information
    extracted_info = {
        "word_count": len(raw_request.split()),
        "has_urgency_keywords": _has_urgency_keywords(raw_request),
        "entities": _extract_entities(raw_request),
        "normalized_text": raw_request.strip(),
    }

    state["raw_request"] = raw_request
    state["current_step"] = "INTAKE"
    state["errors"] = state.get("errors", [])

    logger.info(f"IntakeAgent processed request: {title[:50]}...")

    return state


def _has_urgency_keywords(text):
    urgency_words = [
        "urgent", "emergency", "critical", "broken", "not working",
        "immediately", "asap", "flood", "fire", "leak", "safety",
        "danger", "accident", "injury",
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in urgency_words)


def _extract_entities(text):
    entities = []
    # Simple entity extraction
    block_pattern = r'Block\s+[A-Z]'
    matches = re.findall(block_pattern, text)
    for match in matches:
        entities.append({"type": "location", "value": match})

    return entities
