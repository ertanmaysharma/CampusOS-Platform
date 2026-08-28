"""Request schemas for validation."""
from ..models.request import Request


def validate_create_request(data):
    errors = {}
    if not data.get("title"):
        errors["title"] = "Title is required"
    elif len(data["title"]) > 200:
        errors["title"] = "Title must be 200 characters or less"
    if not data.get("description"):
        errors["description"] = "Description is required"
    if data.get("category") and data["category"] not in Request.CATEGORIES:
        errors["category"] = f"Invalid category. Must be one of: {', '.join(Request.CATEGORIES)}"
    if data.get("priority") and data["priority"] not in Request.PRIORITIES:
        errors["priority"] = f"Invalid priority. Must be one of: {', '.join(Request.PRIORITIES)}"
    return errors
