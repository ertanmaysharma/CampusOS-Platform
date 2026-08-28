from datetime import datetime
from ..extensions import db
from ..models.workflow import Workflow
from ..models.workflow_task import WorkflowTask
from .audit_service import create_audit_log


def get_workflow_by_request(request_id):
    """Get workflow for a request."""
    return Workflow.query.filter_by(request_id=request_id).first()


def get_workflow_by_id(workflow_id):
    """Get workflow by ID."""
    return Workflow.query.get(workflow_id)


def get_workflows(page=1, per_page=20, status=None):
    """Get all workflows with pagination."""
    query = Workflow.query
    if status:
        query = query.filter_by(status=status)
    query = query.order_by(Workflow.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [w.to_dict() for w in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def update_workflow_state(workflow_id, state, agent_name=None, status=None):
    """Update workflow state."""
    workflow = Workflow.query.get(workflow_id)
    if not workflow:
        return None

    old_state = workflow.state
    workflow.state = state
    if agent_name:
        workflow.current_agent = agent_name
    if status:
        workflow.status = status

    if state == "COMPLETED":
        workflow.completed_at = datetime.utcnow()
        workflow.status = "COMPLETED"
    elif state == "FAILED":
        workflow.completed_at = datetime.utcnow()
        workflow.status = "FAILED"

    db.session.commit()
    return workflow


def create_workflow_task(workflow_id, agent_name, task_type, input_data=None):
    """Create a workflow task record."""
    task = WorkflowTask(
        workflow_id=workflow_id,
        agent_name=agent_name,
        task_type=task_type,
        input_data=input_data,
        status="RUNNING",
    )
    db.session.add(task)
    db.session.commit()
    return task


def complete_workflow_task(task_id, output_data=None, error_message=None):
    """Complete a workflow task."""
    task = WorkflowTask.query.get(task_id)
    if not task:
        return None

    task.output_data = output_data
    task.completed_at = datetime.utcnow()
    task.status = "FAILED" if error_message else "COMPLETED"
    task.error_message = error_message

    db.session.commit()
    return task
