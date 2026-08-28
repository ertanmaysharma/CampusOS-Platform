"""Database tools for agents to interact with data."""
from ..models.request import Request
from ..models.user import User
from ..models.department import Department
from ..models.knowledge_document import KnowledgeDocument
from ..extensions import db


def get_request(request_id):
    """Get a request by ID."""
    request = Request.query.get(request_id)
    if not request:
        return None
    return request.to_dict()


def get_related_requests(category=None, department_id=None, limit=5):
    """Get related requests."""
    query = Request.query
    if category:
        query = query.filter_by(category=category)
    if department_id:
        query = query.filter_by(department_id=department_id)
    return [r.to_dict() for r in query.order_by(Request.created_at.desc()).limit(limit).all()]


def get_department(department_id):
    """Get department by ID."""
    dept = Department.query.get(department_id)
    return dept.to_dict() if dept else None


def get_all_departments():
    """Get all active departments."""
    return [d.to_dict() for d in Department.query.filter_by(is_active=True).all()]


def get_user(user_id):
    """Get user by ID."""
    user = User.query.get(user_id)
    return user.to_dict() if user else None
