from ..extensions import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"))
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"))
    action = db.Column(db.String(100), nullable=False, index=True)
    actor_type = db.Column(db.String(30), nullable=False)
    old_value = db.Column(db.JSON)
    new_value = db.Column(db.JSON)
    meta_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship("User", backref="audit_logs")
    workflow = db.relationship("Workflow", backref="audit_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_id": self.request_id,
            "workflow_id": self.workflow_id,
            "action": self.action,
            "actor_type": self.actor_type,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "metadata": self.meta_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user": self.user.to_dict() if self.user else None,
        }
