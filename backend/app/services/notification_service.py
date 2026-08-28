from ..extensions import db
from ..models.notification import Notification


def create_notification(recipient_id, title, message, type, request_id=None):
    """Create a notification."""
    notification = Notification(
        recipient_id=recipient_id,
        request_id=request_id,
        title=title,
        message=message,
        type=type,
    )
    db.session.add(notification)
    db.session.commit()
    return notification


def get_notifications(user_id, unread_only=False, page=1, per_page=20):
    """Get notifications for a user."""
    query = Notification.query.filter_by(recipient_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    query = query.order_by(Notification.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    unread_count = Notification.query.filter_by(recipient_id=user_id, is_read=False).count()

    return {
        "items": [n.to_dict() for n in pagination.items],
        "total": pagination.total,
        "unread_count": unread_count,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def mark_as_read(notification_id, user_id):
    """Mark a notification as read."""
    notification = Notification.query.filter_by(id=notification_id, recipient_id=user_id).first()
    if not notification:
        return False
    notification.is_read = True
    db.session.commit()
    return True


def mark_all_as_read(user_id):
    """Mark all notifications as read for a user."""
    Notification.query.filter_by(recipient_id=user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return True
