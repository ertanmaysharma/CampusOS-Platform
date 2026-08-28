"""Priority Agent - determines request priority."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "PriorityAgent"

CRITICAL_KEYWORDS = ["fire", "flood", "accident", "injury", "danger", "emergency", "collapse", "gas leak"]
HIGH_KEYWORDS = ["broken", "not working", "urgent", "critical", "immediately", "safety", "leak", "severe"]
MEDIUM_KEYWORDS = ["issue", "problem", "need", "request", "please", "fix"]
LOW_KEYWORDS = ["suggestion", "feedback", "when possible", "no rush", "minor"]


def run(state: dict) -> dict:
    """Determine priority based on rules and content analysis."""
    title = state.get("title", "")
    description = state.get("description", "")
    text = f"{title} {description}".lower()

    # Check critical first
    if any(kw in text for kw in CRITICAL_KEYWORDS):
        priority = "CRITICAL"
    elif any(kw in text for kw in HIGH_KEYWORDS):
        priority = "HIGH"
    elif any(kw in text for kw in LOW_KEYWORDS):
        priority = "LOW"
    else:
        priority = "MEDIUM"

    state["priority"] = priority
    state["current_step"] = "PRIORITY"

    logger.info(f"PriorityAgent: Priority set to '{priority}'")
    return state
