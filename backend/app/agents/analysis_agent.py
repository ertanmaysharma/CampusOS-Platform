"""Analysis Agent - analyzes requests and generates recommendations."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "AnalysisAgent"


def run(state: dict) -> dict:
    """Analyze the request and generate recommendations."""
    category = state.get("category", "Other")
    priority = state.get("priority", "MEDIUM")
    title = state.get("title", "")
    description = state.get("description", "")

    # Determine required actions based on category and priority
    actions = _determine_actions(category, priority, title, description)

    # Determine urgency level
    urgency = "immediate" if priority in ("CRITICAL", "HIGH") else "standard"

    analysis = {
        "category": category,
        "priority": priority,
        "urgency": urgency,
        "required_actions": actions,
        "estimated_complexity": "high" if priority in ("CRITICAL", "HIGH") else "medium",
        "requires_human_approval": priority in ("CRITICAL", "HIGH") or category in ("Finance", "Administration"),
    }

    state["analysis"] = analysis
    state["current_step"] = "ANALYSIS"

    logger.info(f"AnalysisAgent: Analysis complete - urgency={urgency}, approval_required={analysis['requires_human_approval']}")
    return state


def _determine_actions(category, priority, title, description):
    actions = []

    action_map = {
        "Maintenance": ["create_maintenance_ticket", "notify_facilities"],
        "Facilities": ["create_facility_ticket", "notify_facilities"],
        "Hostel": ["create_hostel_ticket", "notify_hostel_admin"],
        "Academics": ["create_academic_ticket", "notify_academics"],
        "Finance": ["create_finance_ticket", "notify_finance", "flag_for_review"],
        "IT Support": ["create_it_ticket", "notify_it_team"],
        "Administration": ["create_admin_ticket", "notify_admin"],
        "Lost and Found": ["create_lost_found_ticket", "notify_security"],
        "Student Grievance": ["create_grievance_ticket", "notify_student_affairs"],
    }

    actions = action_map.get(category, ["create_general_ticket", "notify_admin"])

    if priority in ("CRITICAL", "HIGH"):
        actions.append("escalate")

    return actions
