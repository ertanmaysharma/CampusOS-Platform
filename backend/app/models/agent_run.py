from ..extensions import db
from datetime import datetime


class AgentRun(db.Model):
    __tablename__ = "agent_runs"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"))
    agent_name = db.Column(db.String(50), nullable=False)
    task_description = db.Column(db.Text)
    input_data = db.Column(db.JSON)
    output_data = db.Column(db.JSON)
    status = db.Column(db.String(30), default="RUNNING")
    duration_ms = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "agent_name": self.agent_name,
            "task_description": self.task_description,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
