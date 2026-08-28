from ..extensions import db
from datetime import datetime


class Workflow(db.Model):
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False, unique=True)
    state = db.Column(db.String(30), default="INTAKE")
    current_agent = db.Column(db.String(50))
    status = db.Column(db.String(30), default="RUNNING")
    requires_human_approval = db.Column(db.Boolean, default=False)
    approval_status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    tasks = db.relationship("WorkflowTask", backref="workflow", lazy="dynamic",
                            order_by="WorkflowTask.started_at")
    agent_runs = db.relationship("AgentRun", backref="workflow", lazy="dynamic")
    approvals = db.relationship("Approval", backref="workflow", lazy="dynamic")

    STATES = [
        "INTAKE", "CLASSIFICATION", "PRIORITY", "RESEARCH",
        "ROUTING", "ANALYSIS", "ACTION_PLAN", "VERIFICATION",
        "HUMAN_APPROVAL", "EXECUTION", "COMMUNICATION",
        "AUDIT_LOGGING", "COMPLETED", "FAILED"
    ]

    STATUSES = ["RUNNING", "PAUSED", "COMPLETED", "FAILED", "WAITING_APPROVAL"]

    def to_dict(self, include_tasks=False):
        data = {
            "id": self.id,
            "request_id": self.request_id,
            "state": self.state,
            "current_agent": self.current_agent,
            "status": self.status,
            "requires_human_approval": self.requires_human_approval,
            "approval_status": self.approval_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
        if include_tasks:
            data["tasks"] = [t.to_dict() for t in self.tasks.all()]
        return data
