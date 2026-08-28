"""Routing Agent - routes requests to appropriate departments."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "RoutingAgent"


def run(state: dict) -> dict:
    """Route the request to the appropriate department."""
    category = state.get("category", "Other")
    department = state.get("department")

    if not department:
        from ..tools.department_tools import find_department_for_category
        department = find_department_for_category(category)

    if department:
        state["department"] = department
        state["department_id"] = department.get("id")
    else:
        # Default to Administration
        from ..tools.department_tools import find_department_for_category
        admin_dept = find_department_for_category("Administration")
        if admin_dept:
            state["department"] = admin_dept
            state["department_id"] = admin_dept.get("id")

    state["current_step"] = "ROUTING"

    dept_name = state.get("department", {}).get("name", "Unknown") if state.get("department") else "Unknown"
    logger.info(f"RoutingAgent: Routed to '{dept_name}'")
    return state
