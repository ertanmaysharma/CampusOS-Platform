from ..extensions import db
from datetime import datetime


class WorkflowTask(db.Model):
    __tablename__ = "workflow_tasks"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    agent_name = db.Column(db.String(50), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    input_data = db.Column(db.JSON)
    output_data = db.Column(db.JSON)
    status = db.Column(db.String(30), default="PENDING")
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)

    STATUSES = ["PENDING", "RUNNING", "COMPLETED", "FAILED"]

    def to_dict(self):
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "agent_name": self.agent_name,
            "task_type": self.task_type,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
        }
