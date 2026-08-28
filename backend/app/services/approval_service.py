from datetime import datetime
from ..extensions import db
from ..models.approval import Approval
from ..models.workflow import Workflow
from .audit_service import create_audit_log
from .notification_service import create_notification


def create_approval_request(workflow_id, requested_by, reason, proposed_action, risk_level="MEDIUM"):
    """Create an approval request."""
    approval = Approval(
        workflow_id=workflow_id,
        requested_by=requested_by,
        reason=reason,
        proposed_action=proposed_action,
        risk_level=risk_level,
        status="PENDING",
    )
    db.session.add(approval)

    # Update workflow
    workflow = Workflow.query.get(workflow_id)
    if workflow:
        workflow.status = "WAITING_APPROVAL"
        workflow.requires_human_approval = True
        workflow.approval_status = "PENDING"

    db.session.commit()
    return approval


def approve_action(approval_id, reviewer_id, comment=None):
    """Approve an action."""
    approval = Approval.query.get(approval_id)
    if not approval or approval.status != "PENDING":
        return None, "Approval not found or already processed"

    approval.status = "APPROVED"
    approval.reviewed_by = reviewer_id
    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()

    # Update workflow
    workflow = Workflow.query.get(approval.workflow_id)
    if workflow:
        workflow.status = "RUNNING"
        workflow.approval_status = "APPROVED"

    create_audit_log(
        user_id=reviewer_id,
        workflow_id=approval.workflow_id,
        action="APPROVAL_APPROVED",
        actor_type="USER",
        new_value={"approval_id": approval_id, "comment": comment},
    )

    # Notify requester
    if workflow and workflow.request:
        create_notification(
            recipient_id=workflow.request.requester_id,
            title="Request Approved",
            message=f"Your request has been approved by an administrator.",
            type="APPROVAL_APPROVED",
            request_id=workflow.request_id,
        )

    db.session.commit()
    return approval, None


def reject_action(approval_id, reviewer_id, comment=None):
    """Reject an action."""
    approval = Approval.query.get(approval_id)
    if not approval or approval.status != "PENDING":
        return None, "Approval not found or already processed"

    approval.status = "REJECTED"
    approval.reviewed_by = reviewer_id
    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()

    workflow = Workflow.query.get(approval.workflow_id)
    if workflow:
        workflow.status = "FAILED"
        workflow.approval_status = "REJECTED"

    create_audit_log(
        user_id=reviewer_id,
        workflow_id=approval.workflow_id,
        action="APPROVAL_REJECTED",
        actor_type="USER",
        new_value={"approval_id": approval_id, "comment": comment},
    )

    db.session.commit()
    return approval, None


def request_changes(approval_id, reviewer_id, comment):
    """Request changes on an approval."""
    approval = Approval.query.get(approval_id)
    if not approval or approval.status != "PENDING":
        return None, "Approval not found or already processed"

    approval.status = "CHANGES_REQUESTED"
    approval.reviewed_by = reviewer_id
    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()

    db.session.commit()
    return approval, None


def get_pending_approvals(page=1, per_page=20):
    """Get pending approval requests."""
    query = Approval.query.filter_by(status="PENDING").order_by(Approval.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def get_approval_by_id(approval_id):
    """Get approval by ID."""
    return Approval.query.get(approval_id)
