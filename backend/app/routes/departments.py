from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.department import Department
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

departments_bp = Blueprint("departments", __name__)


@departments_bp.route("", methods=["GET"])
@jwt_required()
def list_departments():
    departments = Department.query.filter_by(is_active=True).all()
    return success_response([d.to_dict() for d in departments])


@departments_bp.route("/<int:dept_id>", methods=["GET"])
@jwt_required()
def get_department(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return error_response("Department not found", 404)
    return success_response(dept.to_dict())


@departments_bp.route("", methods=["POST"])
@role_required("ADMIN")
def create_department():
    data = request.get_json()
    if not data or not data.get("name"):
        return error_response("Name is required", 422)

    if Department.query.filter_by(name=data["name"]).first():
        return error_response("Department already exists", 409)

    dept = Department(name=data["name"], description=data.get("description"))
    db.session.add(dept)
    db.session.commit()
    return success_response(dept.to_dict(), "Department created", 201)


@departments_bp.route("/<int:dept_id>", methods=["PATCH"])
@role_required("ADMIN")
def update_department(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return error_response("Department not found", 404)

    data = request.get_json()
    if "name" in data:
        dept.name = data["name"]
    if "description" in data:
        dept.description = data["description"]
    if "is_active" in data:
        dept.is_active = data["is_active"]

    db.session.commit()
    return success_response(dept.to_dict(), "Department updated")
