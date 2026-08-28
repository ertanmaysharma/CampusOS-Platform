"""Workforce Manager - orchestrates the AI agent pipeline."""
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


def process_request(request_id):
    """Run the full agent pipeline for a request."""
    from ..models.request import Request
    from ..models.workflow import Workflow
    from ..models.agent_run import AgentRun
    from ..extensions import db
    from . import intake_agent, classification_agent, priority_agent
    from . import research_agent, routing_agent, analysis_agent
    from . import action_agent, verification_agent, communication_agent

    # Load request
    request = Request.query.get(request_id)
    if not request:
        logger.error(f"Request {request_id} not found")
        return None

    # Get or create workflow
    workflow = Workflow.query.filter_by(request_id=request_id).first()
    if not workflow:
        workflow = Workflow(request_id=request_id, state="INTAKE", status="RUNNING")
        db.session.add(workflow)
        db.session.commit()

    # Initialize state
    state = {
        "request_id": request.id,
        "user_id": request.requester_id,
        "title": request.title,
        "description": request.description,
        "category": request.category,
        "priority": request.priority,
        "workflow_id": workflow.id,
        "current_step": "START",
        "status": "RUNNING",
        "errors": [],
        "retry_count": 0,
    }

    # Define agent pipeline
    agents = [
        ("INTAKE", intake_agent),
        ("CLASSIFICATION", classification_agent),
        ("PRIORITY", priority_agent),
        ("RESEARCH", research_agent),
        ("ROUTING", routing_agent),
        ("ANALYSIS", analysis_agent),
        ("VERIFICATION", verification_agent),
        ("ACTION", action_agent),
        ("COMMUNICATION", communication_agent),
    ]

    # Run through pipeline
    for step_name, agent_module in agents:
        try:
            # Create agent run record
            agent_run = AgentRun(
                workflow_id=workflow.id,
                agent_name=agent_module.AGENT_NAME,
                task_description=f"Processing {step_name}",
                input_data={"step": step_name},
                status="RUNNING",
            )
            db.session.add(agent_run)
            db.session.commit()

            start_time = time.time()

            # Run the agent
            state = agent_module.run(state)

            duration_ms = int((time.time() - start_time) * 1000)

            # Update agent run
            agent_run.output_data = {"step": step_name, "status": "completed"}
            agent_run.status = "COMPLETED"
            agent_run.duration_ms = duration_ms
            agent_run.completed_at = datetime.utcnow()

            # Update workflow state
            workflow.state = step_name
            workflow.current_agent = agent_module.AGENT_NAME

            db.session.commit()

            # Check if approval is needed after verification
            if step_name == "VERIFICATION" and state.get("approval_required"):
                workflow.status = "WAITING_APPROVAL"
                workflow.requires_human_approval = True
                db.session.commit()

                # Notify manager for approval
                _notify_for_approval(state, workflow, request)

                # Update request status
                request.status = "WAITING_FOR_APPROVAL"
                db.session.commit()

                logger.info(f"Workflow {workflow.id} paused for human approval")
                return state

        except Exception as e:
            logger.error(f"Agent {step_name} failed: {str(e)}")
            state["errors"].append(f"{step_name}: {str(e)}")

            # Update agent run with error
            agent_run.status = "FAILED"
            agent_run.error_message = str(e)
            agent_run.completed_at = datetime.utcnow()
            db.session.commit()

            # Update request status
            request.status = "FAILED"
            workflow.status = "FAILED"
            workflow.state = step_name
            db.session.commit()

            return state

    # Update request with final results
    request.category = state.get("category", request.category)
    request.priority = state.get("priority", request.priority)
    request.status = "COMPLETED"

    if state.get("department_id"):
        request.department_id = state["department_id"]

    # Complete workflow
    workflow.state = "COMPLETED"
    workflow.status = "COMPLETED"
    workflow.completed_at = datetime.utcnow()

    # Notify requester
    from ..tools.notification_tools import notify_user
    notify_user(
        request.requester_id,
        "Request Processed",
        state.get("final_response", "Your request has been processed."),
        "REQUEST_COMPLETED",
        request.id,
    )

    # Audit log
    from ..tools.audit_tools import log_audit_event
    log_audit_event(
        user_id=request.requester_id,
        request_id=request.id,
        workflow_id=workflow.id,
        action="WORKFLOW_COMPLETED",
        actor_type="AGENT",
        new_value={"category": state.get("category"), "priority": state.get("priority")},
    )

    db.session.commit()

    logger.info(f"Workflow {workflow.id} completed successfully")
    return state


def _notify_for_approval(state, workflow, request):
    """Notify managers for approval."""
    from ..models.user import User
    from ..models.role import Role
    from ..tools.notification_tools import notify_user
    from ..services.approval_service import create_approval_request

    # Find managers/admins
    admin_role = Role.query.filter_by(name="ADMIN").first()
    if admin_role:
        admins = User.query.filter_by(role_id=admin_role.id, is_active=True).all()
        for admin in admins:
            notify_user(
                admin.id,
                "Approval Required",
                f"Request '{request.title}' requires your approval.",
                "APPROVAL_REQUIRED",
                request.id,
            )

    # Create approval request
    create_approval_request(
        workflow_id=workflow.id,
        requested_by=request.requester_id,
        reason=f"Request requires administrative approval (Priority: {state.get('priority', 'MEDIUM')})",
        proposed_action=state.get("analysis", {}),
        risk_level=state.get("priority", "MEDIUM"),
    )
