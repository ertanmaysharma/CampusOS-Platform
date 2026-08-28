"""Action Agent - performs allowed actions through explicitly defined tools."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "ActionAgent"


def run(state: dict) -> dict:
    """Execute actions based on analysis."""
    request_id = state.get("request_id")
    analysis = state.get("analysis", {})
    actions = analysis.get("required_actions", [])
    category = state.get("category", "Other")

    results = []

    for action in actions:
        result = _execute_action(action, request_id, state)
        results.append(result)

    state["execution_result"] = {
        "actions_executed": len(results),
        "results": results,
        "success": all(r.get("success", False) for r in results),
    }
    state["current_step"] = "EXECUTION"

    logger.info(f"ActionAgent: Executed {len(results)} actions")
    return state


def _execute_action(action_name, request_id, state):
    """Execute a single action through defined tools."""
    try:
        if action_name == "create_maintenance_ticket":
            from ..tools.ticket_tools import create_maintenance_ticket
            return create_maintenance_ticket(request_id, state.get("description", ""))

        elif action_name in ("create_facility_ticket", "create_hostel_ticket",
                             "create_academic_ticket", "create_finance_ticket",
                             "create_it_ticket", "create_admin_ticket",
                             "create_lost_found_ticket", "create_grievance_ticket",
                             "create_general_ticket"):
            from ..tools.ticket_tools import update_request_status
            return update_request_status(request_id, "IN_PROGRESS")

        elif action_name.startswith("notify_"):
            dept_name = action_name.replace("notify_", "").replace("_", " ").title()
            from ..tools.notification_tools import notify_user
            requester_id = state.get("user_id")
            if requester_id:
                notify_user(
                    requester_id,
                    "Request Update",
                    f"Your request has been routed to {dept_name}.",
                    "REQUEST_ROUTED",
                    request_id,
                )
            return {"success": True, "action": action_name}

        elif action_name == "escalate":
            from ..tools.audit_tools import log_audit_event
            log_audit_event(
                request_id=request_id,
                action="REQUEST_ESCALATED",
                actor_type="AGENT",
                new_value={"priority": state.get("priority")},
            )
            return {"success": True, "action": "escalate"}

        elif action_name == "flag_for_review":
            from ..tools.audit_tools import log_audit_event
            log_audit_event(
                request_id=request_id,
                action="REQUEST_FLAGGED_FOR_REVIEW",
                actor_type="AGENT",
                new_value={"reason": "Finance category requires review"},
            )
            return {"success": True, "action": "flag_for_review"}

        else:
            return {"success": False, "error": f"Unknown action: {action_name}"}

    except Exception as e:
        logger.error(f"ActionAgent error executing {action_name}: {str(e)}")
        return {"success": False, "action": action_name, "error": str(e)}
