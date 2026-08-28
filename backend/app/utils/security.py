from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from .errors import error_response


def get_current_user_id():
    identity = get_jwt_identity()
    return int(identity) if identity else None


def role_required(*roles):
    """Decorator to require specific roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            from ..models.user import User
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return error_response("User not found or inactive", 401, "UNAUTHORIZED")
            if user.role.name not in roles:
                return error_response("Insufficient permissions", 403, "FORBIDDEN")
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    """Decorator to require admin role."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from ..models.user import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return error_response("User not found or inactive", 401, "UNAUTHORIZED")
        if user.role.name not in ("ADMIN",):
            return error_response("Admin access required", 403, "FORBIDDEN")
        return fn(*args, **kwargs)
    return wrapper


def manager_or_admin_required(fn):
    """Decorator to require manager or admin role."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from ..models.user import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return error_response("User not found or inactive", 401, "UNAUTHORIZED")
        if user.role.name not in ("ADMIN", "DEPARTMENT_MANAGER"):
            return error_response("Manager or admin access required", 403, "FORBIDDEN")
        return fn(*args, **kwargs)
    return wrapper
