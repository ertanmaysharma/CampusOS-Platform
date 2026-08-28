"""Shared workflow state for LangGraph agents."""
from typing import TypedDict, Optional, List, Dict, Any


class WorkflowState(TypedDict, total=False):
    """State that flows through the agent pipeline."""
    request_id: int
    user_id: int
    raw_request: str
    title: str
    description: str
    category: str
    priority: str
    department: Optional[Dict[str, Any]]
    department_id: Optional[int]
    relevant_context: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    proposed_action: Dict[str, Any]
    verification_result: Dict[str, Any]
    approval_required: bool
    approval_status: Optional[str]
    execution_result: Dict[str, Any]
    notification_result: Dict[str, Any]
    final_response: str
    audit_information: Dict[str, Any]
    errors: List[str]
    retry_count: int
    workflow_id: int
    current_step: str
    status: str
