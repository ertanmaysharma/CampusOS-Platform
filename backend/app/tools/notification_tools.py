"""Notification tools for agents."""
from ..services.notification_service import create_notification


def notify_user(user_id, title, message, notification_type, request_id=None):
    """Create a notification for a user."""
    return create_notification(user_id, title, message, notification_type, request_id)
