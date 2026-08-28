from ..extensions import db
from ..models.audit_log import AuditLog


def create_audit_log(user_id=None, request_id=None, workflow_id=None,
                     action="", actor_type="SYSTEM", old_value=None,
                     new_value=None, metadata=None):
    """Create an audit log entry."""
    log = AuditLog(
        user_id=user_id,
        request_id=request_id,
        workflow_id=workflow_id,
        action=action,
        actor_type=actor_type,
        old_value=old_value,
        new_value=new_value,
        meta_data=metadata,
    )
    db.session.add(log)
    db.session.commit()
    return log


def get_audit_logs(user_id=None, request_id=None, workflow_id=None,
                   action=None, page=1, per_page=50):
    """Get audit logs with filters."""
    query = AuditLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if request_id:
        query = query.filter_by(request_id=request_id)
    if workflow_id:
        query = query.filter_by(workflow_id=workflow_id)
    if action:
        query = query.filter_by(action=action)

    query = query.order_by(AuditLog.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [l.to_dict() for l in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }
