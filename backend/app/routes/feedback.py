from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.feedback import Feedback
from ..utils.errors import error_response, success_response

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("", methods=["POST"])
@jwt_required()
def submit_feedback():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or not data.get("request_id"):
        return error_response("request_id is required", 422)

    feedback = Feedback(
        request_id=data["request_id"],
        workflow_id=data.get("workflow_id"),
        submitted_by=user_id,
        rating=data.get("rating"),
        comment=data.get("comment"),
        correction=data.get("correction"),
    )
    db.session.add(feedback)
    db.session.commit()
    return success_response(feedback.to_dict(), "Feedback submitted", 201)


@feedback_bp.route("", methods=["GET"])
@jwt_required()
def list_feedback():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Feedback.query.order_by(Feedback.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success_response({
        "items": [f.to_dict() for f in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    })
