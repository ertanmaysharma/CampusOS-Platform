"""Department tools for routing agents."""
from ..models.department import Department
from ..models.user import User
from ..extensions import db


def find_department_for_category(category):
    """Map a request category to a department."""
    category_dept_map = {
        "Hostel": "Hostel",
        "Maintenance": "Maintenance",
        "Facilities": "Facilities",
        "Academics": "Academics",
        "Finance": "Finance",
        "Administration": "Administration",
        "IT Support": "IT Support",
    }
    dept_name = category_dept_map.get(category)
    if dept_name:
        dept = Department.query.filter_by(name=dept_name).first()
        if dept:
            return dept.to_dict()
    return None


def get_department_staff(department_id):
    """Get staff members in a department."""
    staff = User.query.filter_by(
        department_id=department_id, is_active=True
    ).all()
    return [u.to_dict() for u in staff]


def get_department_manager(department_id):
    """Get department manager."""
    manager = User.query.filter_by(
        department_id=department_id, is_active=True
    ).join(User.role).filter(
        User.role.has(name="DEPARTMENT_MANAGER")
    ).first()
    return manager.to_dict() if manager else None
