from ..extensions import db
from datetime import datetime


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"))
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    comment = db.Column(db.Text)
    correction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submitter = db.relationship("User", backref="feedback_submitted")
    workflow = db.relationship("Workflow", backref="feedback_entries")

    def to_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "workflow_id": self.workflow_id,
            "submitted_by": self.submitted_by,
            "rating": self.rating,
            "comment": self.comment,
            "correction": self.correction,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "submitter": self.submitter.to_dict() if self.submitter else None,
        }
