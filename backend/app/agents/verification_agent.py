"""Verification Agent - critical safety layer that verifies agent outputs."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "VerificationAgent"


def run(state: dict) -> dict:
    """Verify the workflow outputs and determine if approval is needed."""
    issues = []

    # Verify classification
    category = state.get("category")
    if not category:
        issues.append("Missing category classification")

    # Verify priority
    priority = state.get("priority")
    valid_priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    if priority not in valid_priorities:
        issues.append(f"Invalid priority: {priority}")

    # Verify routing
    department = state.get("department")
    if not department:
        issues.append("No department assigned")

    # Verify analysis
    analysis = state.get("analysis", {})
    if not analysis:
        issues.append("No analysis performed")

    # Determine result
    requires_approval = analysis.get("requires_human_approval", False)

    if issues:
        result = {
            "status": "needs_human_review",
            "issues": issues,
            "requires_approval": True,
        }
        state["approval_required"] = True
    elif requires_approval:
        result = {
            "status": "approved",
            "issues": [],
            "requires_approval": True,
        }
        state["approval_required"] = True
    else:
        result = {
            "status": "approved",
            "issues": [],
            "requires_approval": False,
        }
        state["approval_required"] = False

    state["verification_result"] = result
    state["current_step"] = "VERIFICATION"

    logger.info(f"VerificationAgent: Status={result['status']}, approval_required={result['requires_approval']}")
    return state
