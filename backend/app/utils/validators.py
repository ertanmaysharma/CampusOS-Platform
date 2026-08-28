import re


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    return errors


def validate_request_data(data, required_fields=None):
    errors = {}
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f"{field} is required"
    if "email" in data and data["email"] and not validate_email(data["email"]):
        errors["email"] = "Invalid email format"
    if "password" in data and data["password"]:
        pw_errors = validate_password(data["password"])
        if pw_errors:
            errors["password"] = pw_errors
    return errors
