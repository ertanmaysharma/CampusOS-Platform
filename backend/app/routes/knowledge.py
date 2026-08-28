from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.knowledge_service import (
    create_document, get_documents, get_document_by_id,
    update_document, delete_document
)
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

knowledge_bp = Blueprint("knowledge", __name__)


@knowledge_bp.route("", methods=["GET"])
@jwt_required()
def list_documents():
    category = request.args.get("category")
    department_id = request.args.get("department_id", type=int)
    search = request.args.get("search")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    result = get_documents(
        category=category, department_id=department_id,
        search=search, page=page, per_page=per_page
    )
    return success_response(result)


@knowledge_bp.route("", methods=["POST"])
@role_required("ADMIN")
def create():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return error_response("Title and content are required", 422)
    doc = create_document(data)
    return success_response(doc.to_dict(), "Document created", 201)


@knowledge_bp.route("/<int:doc_id>", methods=["GET"])
@jwt_required()
def get_document(doc_id):
    doc = get_document_by_id(doc_id)
    if not doc:
        return error_response("Document not found", 404)
    return success_response(doc.to_dict())


@knowledge_bp.route("/<int:doc_id>", methods=["PATCH"])
@role_required("ADMIN")
def update(doc_id):
    data = request.get_json()
    doc, error = update_document(doc_id, data)
    if error:
        return error_response(error, 404)
    return success_response(doc.to_dict(), "Document updated")


@knowledge_bp.route("/<int:doc_id>", methods=["DELETE"])
@role_required("ADMIN")
def delete(doc_id):
    success, error = delete_document(doc_id)
    if not success:
        return error_response(error, 404)
    return success_response(None, "Document deleted")
