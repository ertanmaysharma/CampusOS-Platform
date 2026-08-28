from ..extensions import db
from datetime import datetime


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    priority = db.Column(db.String(20), default="MEDIUM", index=True)
    status = db.Column(db.String(30), default="NEW", index=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    workflow = db.relationship("Workflow", backref="request", uselist=False, lazy="joined")
    feedback_entries = db.relationship("Feedback", backref="request", lazy="dynamic")
    notifications = db.relationship("Notification", backref="request", lazy="dynamic")
    audit_logs = db.relationship("AuditLog", backref="request", lazy="dynamic")

    STATUSES = [
        "NEW", "CLASSIFYING", "ANALYZING", "ROUTING",
        "WAITING_FOR_APPROVAL", "APPROVED", "IN_PROGRESS",
        "COMPLETED", "REJECTED", "FAILED", "CANCELLED"
    ]

    CATEGORIES = [
        "Hostel", "Maintenance", "Facilities", "Academics",
        "Finance", "Administration", "IT Support", "Lost and Found",
        "Student Grievance", "Other"
    ]

    PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def to_dict(self, include_workflow=False):
        data = {
            "id": self.id,
            "request_number": self.request_number,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "requester": self.requester.to_dict() if self.requester else None,
            "assignee": self.assignee.to_dict() if self.assignee else None,
            "department": self.department.to_dict() if self.department else None,
        }
        if include_workflow and self.workflow:
            data["workflow"] = self.workflow.to_dict()
        return data
