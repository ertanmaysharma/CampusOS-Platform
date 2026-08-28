from ..extensions import db
from ..models.knowledge_document import KnowledgeDocument


def create_document(data):
    """Create a knowledge document."""
    doc = KnowledgeDocument(
        title=data["title"],
        content=data["content"],
        category=data.get("category", "General"),
        department_id=data.get("department_id"),
        meta_data=data.get("metadata"),
    )
    db.session.add(doc)
    db.session.commit()
    return doc


def get_documents(category=None, department_id=None, search=None, page=1, per_page=20):
    """Get knowledge documents."""
    query = KnowledgeDocument.query
    if category:
        query = query.filter_by(category=category)
    if department_id:
        query = query.filter_by(department_id=department_id)
    if search:
        query = query.filter(
            db.or_(
                KnowledgeDocument.title.ilike(f"%{search}%"),
                KnowledgeDocument.content.ilike(f"%{search}%"),
            )
        )
    query = query.order_by(KnowledgeDocument.updated_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [d.to_dict() for d in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def get_document_by_id(doc_id):
    """Get document by ID."""
    return KnowledgeDocument.query.get(doc_id)


def update_document(doc_id, data):
    """Update a knowledge document."""
    doc = KnowledgeDocument.query.get(doc_id)
    if not doc:
        return None, "Document not found"
    for field in ["title", "content", "category", "department_id", "meta_data"]:
        if field in data:
            setattr(doc, field, data[field])
    db.session.commit()
    return doc, None


def delete_document(doc_id):
    """Delete a knowledge document."""
    doc = KnowledgeDocument.query.get(doc_id)
    if not doc:
        return False, "Document not found"
    db.session.delete(doc)
    db.session.commit()
    return True, None


def search_knowledge(query_text, category=None):
    """Search knowledge base for agents."""
    query = KnowledgeDocument.query.filter(
        db.or_(
            KnowledgeDocument.title.ilike(f"%{query_text}%"),
            KnowledgeDocument.content.ilike(f"%{query_text}%"),
        )
    )
    if category:
        query = query.filter_by(category=category)
    return query.limit(5).all()
