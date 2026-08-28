from datetime import datetime
from ..extensions import db
from ..models.agent_run import AgentRun


def create_agent_run(workflow_id, agent_name, task_description=None, input_data=None):
    """Create an agent run record."""
    run = AgentRun(
        workflow_id=workflow_id,
        agent_name=agent_name,
        task_description=task_description,
        input_data=input_data,
        status="RUNNING",
    )
    db.session.add(run)
    db.session.commit()
    return run


def complete_agent_run(run_id, output_data=None, error_message=None, duration_ms=None):
    """Complete an agent run."""
    run = AgentRun.query.get(run_id)
    if not run:
        return None
    run.output_data = output_data
    run.error_message = error_message
    run.duration_ms = duration_ms
    run.status = "FAILED" if error_message else "COMPLETED"
    run.completed_at = datetime.utcnow()
    db.session.commit()
    return run


def get_agent_runs(workflow_id=None, agent_name=None, page=1, per_page=20):
    """Get agent runs."""
    query = AgentRun.query
    if workflow_id:
        query = query.filter_by(workflow_id=workflow_id)
    if agent_name:
        query = query.filter_by(agent_name=agent_name)
    query = query.order_by(AgentRun.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [r.to_dict() for r in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def get_agent_status():
    """Get overall agent status."""
    agents = [
        "IntakeAgent", "ClassificationAgent", "PriorityAgent",
        "ResearchAgent", "RoutingAgent", "AnalysisAgent",
        "ActionAgent", "VerificationAgent", "CommunicationAgent",
        "AnalyticsAgent", "FeedbackAgent",
    ]
    status = []
    for agent in agents:
        latest = AgentRun.query.filter_by(agent_name=agent)\
            .order_by(AgentRun.created_at.desc()).first()
        status.append({
            "name": agent,
            "last_run": latest.created_at.isoformat() if latest else None,
            "last_status": latest.status if latest else "idle",
        })
    return status
