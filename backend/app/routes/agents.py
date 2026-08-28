from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.agent_service import get_agent_runs, get_agent_status
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

agents_bp = Blueprint("agents", __name__)


@agents_bp.route("", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def list_agents():
    status = get_agent_status()
    return success_response(status)


@agents_bp.route("/status", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def agents_status():
    status = get_agent_status()
    return success_response(status)


@agents_bp.route("/runs", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def list_runs():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    workflow_id = request.args.get("workflow_id", type=int)
    agent_name = request.args.get("agent_name")

    result = get_agent_runs(
        workflow_id=workflow_id,
        agent_name=agent_name,
        page=page,
        per_page=per_page,
    )
    return success_response(result)


@agents_bp.route("/runs/<int:run_id>", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def get_run(run_id):
    from ..models.agent_run import AgentRun
    run = AgentRun.query.get(run_id)
    if not run:
        return error_response("Agent run not found", 404)
    return success_response(run.to_dict())
