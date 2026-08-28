"""Ticket tools for agents."""
from ..models.request import Request
from ..models.workflow import Workflow
from ..extensions import db


def update_request_status(request_id, status, assigned_to=None, department_id=None):
    """Update request status and assignment."""
    request = Request.query.get(request_id)
    if not request:
        return {"success": False, "error": "Request not found"}

    request.status = status
    if assigned_to:
        request.assigned_to = assigned_to
    if department_id:
        request.department_id = department_id

    db.session.commit()
    return {"success": True, "request": request.to_dict()}


def create_maintenance_ticket(request_id, description):
    """Create a maintenance ticket (workflow task)."""
    request = Request.query.get(request_id)
    if not request:
        return {"success": False, "error": "Request not found"}

    # Create workflow task for maintenance
    workflow = request.workflow
    if workflow:
        from ..models.workflow_task import WorkflowTask
        task = WorkflowTask(
            workflow_id=workflow.id,
            agent_name="ActionAgent",
            task_type="MAINTENANCE_TICKET",
            input_data={"request_id": request_id, "description": description},
            output_data={"ticket_created": True, "ticket_type": "MAINTENANCE"},
            status="COMPLETED",
        )
        db.session.add(task)

    request.status = "IN_PROGRESS"
    db.session.commit()
    return {"success": True, "ticket_type": "MAINTENANCE", "request_id": request_id}
