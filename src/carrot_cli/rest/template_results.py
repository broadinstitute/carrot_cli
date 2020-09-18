import logging
from . import request_handler

LOGGER = logging.getLogger(__name__)

def create_map(
    template_id,
    result_id,
    result_key
):
    """Submits a request to CARROT's template_result create mapping"""
    return request_handler.create_map(
        "templates",
        template_id,
        "results",
        result_id,
        {
            "result_key":result_key
        }
    )
