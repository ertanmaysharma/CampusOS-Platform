from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..services.request_service import (
    create_request, get_requests, get_request_by_id,
    update_request, cancel_request, get_request_stats
)
from ..services.workflow_service import get_workflow_by_request
from ..agents.workforce_manager import process_request
from ..utils.errors import error_response, success_response
from ..schemas.requests import validate_create_request

requests_bp = Blueprint("requests", __name__)


@requests_bp.route("", methods=["POST"])
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400)

    errors = validate_create_request(data)
    if errors:
        return error_response("Validation failed", 422, "VALIDATION_ERROR", errors)

    req = create_request(user_id, data)
    return success_response(req.to_dict(), "Request created", 201)


@requests_bp.route("", methods=["GET"])
@jwt_required()
def list_requests():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    status = request.args.get("status")
    category = request.args.get("category")
    priority = request.args.get("priority")
    department_id = request.args.get("department_id", type=int)

    result = get_requests(
        user_id=user_id,
        role_name=user.role.name,
        status=status,
        category=category,
        priority=priority,
        department_id=department_id,
        page=page,
        per_page=per_page,
    )
    return success_response(result)


@requests_bp.route("/<int:req_id>", methods=["GET"])
@jwt_required()
def get_request(req_id):
    req = get_request_by_id(req_id)
    if not req:
        return error_response("Request not found", 404)
    return success_response(req.to_dict(include_workflow=True))


@requests_bp.route("/<int:req_id>", methods=["PATCH"])
@jwt_required()
def update(req_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400)

    req, error = update_request(req_id, user_id, data)
    if error:
        return error_response(error, 400 if "not found" in error.lower() else 422)
    return success_response(req.to_dict(), "Request updated")


@requests_bp.route("/<int:req_id>", methods=["DELETE"])
@jwt_required()
def cancel(req_id):
    user_id = int(get_jwt_identity())
    req, error = cancel_request(req_id, user_id)
    if error:
        return error_response(error, 400 if "not found" in error.lower() else 422)
    return success_response(req.to_dict(), "Request cancelled")


@requests_bp.route("/<int:req_id>/process", methods=["POST"])
@jwt_required()
def process(req_id):
    user_id = int(get_jwt_identity())
    req = get_request_by_id(req_id)
    if not req:
        return error_response("Request not found", 404)

    # Process through AI workflow
    state = process_request(req_id)
    if state:
        return success_response(
            {
                "category": state.get("category"),
                "priority": state.get("priority"),
                "department": state.get("department"),
                "status": state.get("status"),
                "final_response": state.get("final_response"),
                "approval_required": state.get("approval_required"),
            },
            "Request processed"
        )
    return error_response("Processing failed", 500)
