from datetime import datetime, timedelta
from sqlalchemy import func
from ..extensions import db
from ..models.request import Request
from ..models.workflow import Workflow
from ..models.agent_run import AgentRun
from ..models.approval import Approval
from ..models.notification import Notification
from ..models.user import User
from ..models.department import Department


def get_student_dashboard(user_id):
    """Get dashboard data for students."""
    from ..services.request_service import get_request_stats
    stats = get_request_stats(user_id=user_id, role_name="STUDENT")

    recent_requests = Request.query.filter_by(requester_id=user_id)\
        .order_by(Request.created_at.desc()).limit(5).all()

    unread_notifications = Notification.query.filter_by(
        recipient_id=user_id, is_read=False
    ).count()

    return {
        "stats": stats,
        "recent_requests": [r.to_dict() for r in recent_requests],
        "unread_notifications": unread_notifications,
    }


def get_staff_dashboard(user_id):
    """Get dashboard data for staff."""
    assigned = Request.query.filter_by(assigned_to=user_id)\
        .filter(Request.status.in_(["IN_PROGRESS", "APPROVED"])).count()

    pending_tasks = Request.query.filter_by(assigned_to=user_id)\
        .filter_by(status="IN_PROGRESS").count()

    completed = Request.query.filter_by(assigned_to=user_id)\
        .filter_by(status="COMPLETED").count()

    recent_assigned = Request.query.filter_by(assigned_to=user_id)\
        .order_by(Request.created_at.desc()).limit(5).all()

    return {
        "assigned_count": assigned,
        "pending_tasks": pending_tasks,
        "completed": completed,
        "recent_assigned": [r.to_dict() for r in recent_assigned],
    }


def get_manager_dashboard(user_id):
    """Get dashboard data for department managers."""
    from ..models.user import User as UserModel
    user = UserModel.query.get(user_id)
    dept_id = user.department_id if user else None

    dept_requests = Request.query.filter_by(department_id=dept_id).count() if dept_id else 0
    pending_approvals = Approval.query.filter_by(status="PENDING").count()
    dept_in_progress = Request.query.filter_by(department_id=dept_id)\
        .filter(Request.status.in_(["IN_PROGRESS", "APPROVED"])).count() if dept_id else 0

    return {
        "department_requests": dept_requests,
        "pending_approvals": pending_approvals,
        "in_progress": dept_in_progress,
    }


def get_admin_dashboard():
    """Get dashboard data for administrators."""
    total_requests = Request.query.count()
    open_requests = Request.query.filter(
        Request.status.in_(["NEW", "CLASSIFYING", "ANALYZING", "ROUTING"])
    ).count()
    pending_approvals = Approval.query.filter_by(status="PENDING").count()

    today = datetime.utcnow().date()
    resolved_today = Request.query.filter(
        Request.resolved_at >= datetime.combine(today, datetime.min.time()),
        Request.status == "COMPLETED",
    ).count()

    # Category distribution
    category_dist = db.session.query(
        Request.category, func.count(Request.id)
    ).group_by(Request.category).all()

    # Priority distribution
    priority_dist = db.session.query(
        Request.priority, func.count(Request.id)
    ).group_by(Request.priority).all()

    # Status distribution
    status_dist = db.session.query(
        Request.status, func.count(Request.id)
    ).group_by(Request.status).all()

    # Department workload
    dept_workload = db.session.query(
        Department.name, func.count(Request.id)
    ).join(Request, Request.department_id == Department.id, isouter=True)\
     .group_by(Department.name).all()

    # Recent requests
    recent_requests = Request.query.order_by(Request.created_at.desc()).limit(10).all()

    # Recent agent activity
    recent_agents = AgentRun.query.order_by(AgentRun.created_at.desc()).limit(10).all()

    # Failed workflows
    failed_workflows = Workflow.query.filter_by(status="FAILED").count()

    # Average resolution time
    resolved_requests = Request.query.filter(
        Request.resolved_at.isnot(None), Request.created_at.isnot(None)
    ).all()
    avg_resolution = None
    if resolved_requests:
        total_hours = sum(
            (r.resolved_at - r.created_at).total_seconds() / 3600
            for r in resolved_requests
        )
        avg_resolution = round(total_hours / len(resolved_requests), 1)

    return {
        "total_requests": total_requests,
        "open_requests": open_requests,
        "pending_approvals": pending_approvals,
        "resolved_today": resolved_today,
        "category_distribution": {c: count for c, count in category_dist},
        "priority_distribution": {p: count for p, count in priority_dist},
        "status_distribution": {s: count for s, count in status_dist},
        "department_workload": {d: count for d, count in dept_workload},
        "recent_requests": [r.to_dict() for r in recent_requests],
        "recent_agents": [a.to_dict() for a in recent_agents],
        "failed_workflows": failed_workflows,
        "average_resolution_hours": avg_resolution,
        "total_users": User.query.count(),
        "total_departments": Department.query.count(),
    }
