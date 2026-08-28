"""LangGraph workflow graph for CampusOS."""
import logging

logger = logging.getLogger(__name__)

# Agent pipeline definition
AGENT_PIPELINE = [
    "INTAKE",
    "CLASSIFICATION",
    "PRIORITY",
    "RESEARCH",
    "ROUTING",
    "ANALYSIS",
    "VERIFICATION",
    "ACTION",
    "COMMUNICATION",
    "AUDIT_LOGGING",
    "COMPLETED",
]


def get_pipeline_steps():
    """Get the ordered pipeline steps."""
    return AGENT_PIPELINE


def get_step_index(step_name):
    """Get the index of a step in the pipeline."""
    try:
        return AGENT_PIPELINE.index(step_name)
    except ValueError:
        return -1


def get_next_step(current_step):
    """Get the next step in the pipeline."""
    idx = get_step_index(current_step)
    if idx >= 0 and idx < len(AGENT_PIPELINE) - 1:
        return AGENT_PIPELINE[idx + 1]
    return None


def get_previous_step(current_step):
    """Get the previous step in the pipeline."""
    idx = get_step_index(current_step)
    if idx > 0:
        return AGENT_PIPELINE[idx - 1]
    return None
