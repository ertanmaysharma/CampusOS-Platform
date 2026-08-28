import random
import string
from datetime import datetime
from ..extensions import db
from ..models.request import Request
from ..models.workflow import Workflow
from .audit_service import create_audit_log
from .notification_service import create_notification


def generate_request_number():
    """Generate a unique request number."""
    num = random.randint(1000, 9999)
    return f"REQ-{num}"


def create_request(user_id, data):
    """Create a new campus request."""
    request_number = generate_request_number()
    # Ensure uniqueness
    while Request.query.filter_by(request_number=request_number).first():
        request_number = generate_request_number()

    request = Request(
        request_number=request_number,
        requester_id=user_id,
        title=data["title"],
        description=data["description"],
        category=data.get("category", "Other"),
        priority=data.get("priority", "MEDIUM"),
        status="NEW",
        department_id=data.get("department_id"),
    )

    db.session.add(request)
    db.session.flush()

    # Create associated workflow
    workflow = Workflow(
        request_id=request.id,
        state="INTAKE",
        status="RUNNING",
    )
    db.session.add(workflow)

    # Audit log
    create_audit_log(
        user_id=user_id,
        request_id=request.id,
        action="REQUEST_CREATED",
        actor_type="USER",
        new_value={"title": request.title, "category": request.category},
    )

    db.session.commit()
    return request


def get_requests(user_id=None, role_name=None, status=None, category=None,
                 priority=None, department_id=None, page=1, per_page=20):
    """Get requests with filters."""
    query = Request.query

    if user_id and role_name == "STUDENT":
        query = query.filter_by(requester_id=user_id)
    elif user_id and role_name == "STAFF":
        query = query.filter_by(assigned_to=user_id)

    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
    if priority:
        query = query.filter_by(priority=priority)
    if department_id:
        query = query.filter_by(department_id=department_id)

    query = query.order_by(Request.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [r.to_dict() for r in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def get_request_by_id(request_id):
    """Get a single request by ID."""
    return Request.query.get(request_id)


def update_request(request_id, user_id, data):
    """Update a request."""
    request = Request.query.get(request_id)
    if not request:
        return None, "Request not found"

    old_values = {}
    new_values = {}

    updatable_fields = ["title", "description", "category", "priority", "status", "department_id", "assigned_to"]
    for field in updatable_fields:
        if field in data:
            old_values[field] = getattr(request, field)
            setattr(request, field, data[field])
            new_values[field] = data[field]

    if "status" in data and data["status"] == "COMPLETED":
        request.resolved_at = datetime.utcnow()

    create_audit_log(
        user_id=user_id,
        request_id=request.id,
        action="REQUEST_UPDATED",
        actor_type="USER",
        old_value=old_values,
        new_value=new_values,
    )

    db.session.commit()
    return request, None


def cancel_request(request_id, user_id):
    """Cancel a request."""
    request = Request.query.get(request_id)
    if not request:
        return None, "Request not found"

    request.status = "CANCELLED"
    request.resolved_at = datetime.utcnow()

    create_audit_log(
        user_id=user_id,
        request_id=request.id,
        action="REQUEST_CANCELLED",
        actor_type="USER",
        old_value={"status": request.status},
        new_value={"status": "CANCELLED"},
    )

    db.session.commit()
    return request, None


def get_request_stats(user_id=None, role_name=None):
    """Get request statistics."""
    query = Request.query
    if user_id and role_name == "STUDENT":
        query = query.filter_by(requester_id=user_id)

    total = query.count()
    open_count = query.filter(Request.status.in_(["NEW", "CLASSIFYING", "ANALYZING", "ROUTING"])).count()
    in_progress = query.filter(Request.status.in_(["IN_PROGRESS", "APPROVED", "WAITING_FOR_APPROVAL"])).count()
    resolved = query.filter_by(status="COMPLETED").count()
    pending = query.filter_by(status="WAITING_FOR_APPROVAL").count()

    # Category distribution
    from sqlalchemy import func
    category_dist = db.session.query(
        Request.category, func.count(Request.id)
    ).group_by(Request.category).all()

    priority_dist = db.session.query(
        Request.priority, func.count(Request.id)
    ).group_by(Request.priority).all()

    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "pending": pending,
        "category_distribution": {c: count for c, count in category_dist},
        "priority_distribution": {p: count for p, count in priority_dist},
    }
