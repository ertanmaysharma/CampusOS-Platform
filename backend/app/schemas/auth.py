"""Auth request/response schemas."""


def validate_register(data):
    errors = {}
    if not data.get("name"):
        errors["name"] = "Name is required"
    if not data.get("email"):
        errors["email"] = "Email is required"
    if not data.get("password"):
        errors["password"] = "Password is required"
    if data.get("password") != data.get("confirm_password"):
        errors["confirm_password"] = "Passwords do not match"
    return errors


def validate_login(data):
    errors = {}
    if not data.get("email"):
        errors["email"] = "Email is required"
    if not data.get("password"):
        errors["password"] = "Password is required"
    return errors
