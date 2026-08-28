"""Research Agent - retrieves relevant information from knowledge base and database."""
import logging

logger = logging.getLogger(__name__)

AGENT_NAME = "ResearchAgent"


def run(state: dict) -> dict:
    """Research the request using knowledge base and database."""
    category = state.get("category", "Other")
    title = state.get("title", "")
    description = state.get("description", "")

    # Search knowledge base
    try:
        from ..tools.knowledge_tools import search_knowledge_base
        kb_results = search_knowledge_base(f"{title} {description}")
    except Exception:
        kb_results = []

    # Get related requests
    try:
        from ..tools.database_tools import get_related_requests
        related = get_related_requests(category=category, limit=3)
    except Exception:
        related = []

    # Get department info
    try:
        from ..tools.department_tools import find_department_for_category
        dept = find_department_for_category(category)
    except Exception:
        dept = None

    state["relevant_context"] = {
        "knowledge_base": kb_results,
        "related_requests": related,
        "department": dept,
    }
    state["department"] = dept
    state["department_id"] = dept["id"] if dept else None
    state["current_step"] = "RESEARCH"

    logger.info(f"ResearchAgent: Found {len(kb_results)} KB results, {len(related)} related requests")
    return state
