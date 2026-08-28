from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt,
    create_access_token, create_refresh_token
)
from ..services.auth_service import register_user, login_user, change_password, get_current_user
from ..utils.errors import error_response, success_response
from ..schemas.auth import validate_register, validate_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400, "BAD_REQUEST")

    validation_errors = validate_register(data)
    if validation_errors:
        return error_response("Validation failed", 422, "VALIDATION_ERROR", validation_errors)

    user, errors = register_user(data)
    if errors:
        return error_response("Registration failed", 422, "REGISTRATION_ERROR", errors)

    return success_response(user.to_dict(), "Registration successful", 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400, "BAD_REQUEST")

    validation_errors = validate_login(data)
    if validation_errors:
        return error_response("Validation failed", 422, "VALIDATION_ERROR", validation_errors)

    result, error = login_user(data["email"], data["password"])
    if error:
        return error_response(error, 401, "LOGIN_FAILED")

    return success_response(result, "Login successful")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = int(get_jwt_identity())
    claims = get_jwt()
    access_token = create_access_token(
        identity=identity,
        additional_claims={"role": claims.get("role"), "email": claims.get("email")}
    )
    return success_response({"access_token": access_token}, "Token refreshed")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user_data = get_current_user(user_id)
    if not user_data:
        return error_response("User not found", 404, "NOT_FOUND")
    return success_response(user_data)


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password_route():
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400, "BAD_REQUEST")

    user_id = int(get_jwt_identity())
    success, error = change_password(
        user_id,
        data.get("current_password", ""),
        data.get("new_password", "")
    )

    if not success:
        return error_response(error if isinstance(error, str) else "Password change failed", 400, "PASSWORD_CHANGE_FAILED", error if isinstance(error, dict) else None)

    return success_response(None, "Password changed successfully")
