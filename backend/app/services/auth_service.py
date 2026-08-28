from datetime import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from ..extensions import db
from ..models.user import User
from ..models.role import Role
from ..utils.validators import validate_email, validate_password


def register_user(data):
    """Register a new user."""
    errors = {}

    # Validate required fields
    for field in ["name", "email", "password"]:
        if not data.get(field):
            errors[field] = f"{field} is required"

    if not validate_email(data.get("email", "")):
        errors["email"] = "Invalid email format"

    pw_errors = validate_password(data.get("password", ""))
    if pw_errors:
        errors["password"] = pw_errors

    if data.get("password") != data.get("confirm_password"):
        errors["confirm_password"] = "Passwords do not match"

    if errors:
        return None, errors

    # Check duplicate email
    if User.query.filter_by(email=data["email"]).first():
        return None, {"email": "Email already registered"}

    # Determine allowed role - only STUDENT and FACULTY for public registration
    role_name = data.get("role", "STUDENT").upper()
    if role_name not in ("STUDENT", "FACULTY"):
        role_name = "STUDENT"

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        role = Role.query.filter_by(name="STUDENT").first()

    user = User(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        role_id=role.id,
        department_id=data.get("department_id"),
        is_active=True,
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return user, None


def login_user(email, password):
    """Authenticate user and return tokens."""
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None, "Invalid email or password"

    if not user.is_active:
        return None, "Account is deactivated"

    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()

    # Create tokens
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role.name, "email": user.email}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={"role": user.role.name}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict(),
    }, None


def change_password(user_id, current_password, new_password):
    """Change user password."""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    if not user.check_password(current_password):
        return False, "Current password is incorrect"

    pw_errors = validate_password(new_password)
    if pw_errors:
        return False, pw_errors

    user.set_password(new_password)
    db.session.commit()
    return True, None


def get_current_user(user_id):
    """Get current user info."""
    user = User.query.get(user_id)
    if not user:
        return None
    return user.to_dict()
