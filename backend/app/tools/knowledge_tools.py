"""Knowledge tools for research agents."""
from ..services.knowledge_service import search_knowledge


def search_knowledge_base(query_text, category=None):
    """Search the knowledge base."""
    results = search_knowledge(query_text, category)
    return [{"id": r.id, "title": r.title, "content": r.content[:500], "category": r.category} for r in results]
