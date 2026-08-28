"""Communication Agent - generates user-facing messages."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "CommunicationAgent"


def run(state: dict) -> dict:
    """Generate communication messages."""
    category = state.get("category", "Other")
    priority = state.get("priority", "MEDIUM")
    status = state.get("verification_result", {}).get("status", "approved")
    department = state.get("department", {})
    dept_name = department.get("name", "the appropriate department") if department else "the appropriate department"

    # Generate final response
    if status == "approved":
        if state.get("approval_required"):
            response = (
                f"Your {category.lower()} request has been reviewed and is awaiting "
                f"administrative approval before being processed by {dept_name}. "
                f"You will be notified once an action is taken."
            )
        else:
            response = (
                f"Your {category.lower()} request has been processed and routed to "
                f"{dept_name}. The team will address this shortly."
            )
    else:
        response = (
            f"Your request requires additional review. Our team will examine "
            f"the details and get back to you soon."
        )

    state["final_response"] = response
    state["current_step"] = "COMMUNICATION"

    logger.info(f"CommunicationAgent: Generated response for request")
    return state
