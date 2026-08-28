"""Audit tools for agents."""
from ..services.audit_service import create_audit_log


def log_audit_event(user_id=None, request_id=None, workflow_id=None,
                    action="", actor_type="AGENT", new_value=None, metadata=None):
    """Log an audit event."""
    return create_audit_log(
        user_id=user_id,
        request_id=request_id,
        workflow_id=workflow_id,
        action=action,
        actor_type=actor_type,
        new_value=new_value,
        metadata=metadata,
    )
