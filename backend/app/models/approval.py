from ..extensions import db
from datetime import datetime


class Approval(db.Model):
    __tablename__ = "approvals"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(30), default="PENDING", index=True)
    reason = db.Column(db.Text)
    proposed_action = db.Column(db.JSON)
    risk_level = db.Column(db.String(20), default="MEDIUM")
    reviewer_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)

    requester_user = db.relationship("User", foreign_keys=[requested_by], backref="requested_approvals")
    reviewer_user = db.relationship("User", foreign_keys=[reviewed_by], backref="reviewed_approvals")

    STATUSES = ["PENDING", "APPROVED", "REJECTED", "CHANGES_REQUESTED"]

    def to_dict(self):
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "requested_by": self.requested_by,
            "reviewed_by": self.reviewed_by,
            "status": self.status,
            "reason": self.reason,
            "proposed_action": self.proposed_action,
            "risk_level": self.risk_level,
            "reviewer_comment": self.reviewer_comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "requester": self.requester_user.to_dict() if self.requester_user else None,
            "reviewer": self.reviewer_user.to_dict() if self.reviewer_user else None,
        }
