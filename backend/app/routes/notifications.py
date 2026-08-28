from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.notification_service import get_notifications, mark_as_read, mark_all_as_read
from ..utils.errors import error_response, success_response

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("", methods=["GET"])
@jwt_required()
def list_notifications():
    user_id = int(get_jwt_identity())
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    unread_only = request.args.get("unread_only", "false").lower() == "true"

    result = get_notifications(user_id, unread_only=unread_only, page=page, per_page=per_page)
    return success_response(result)


@notifications_bp.route("/<int:notif_id>/read", methods=["PATCH"])
@jwt_required()
def read_notification(notif_id):
    user_id = int(get_jwt_identity())
    success = mark_as_read(notif_id, user_id)
    if not success:
        return error_response("Notification not found", 404)
    return success_response(None, "Marked as read")


@notifications_bp.route("/read-all", methods=["PATCH"])
@jwt_required()
def read_all():
    user_id = int(get_jwt_identity())
    mark_all_as_read(user_id)
    return success_response(None, "All notifications marked as read")
