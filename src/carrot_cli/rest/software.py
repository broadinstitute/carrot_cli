import logging
from . import request_handler

LOGGER = logging.getLogger(__name__)

def find_by_id(software_id):
    """Submits a request to CARROT's software find_by_id mapping"""
    return request_handler.find_by_id("softwares", software_id)

def find(
    software_id,
    name,
    description,
    repository_url,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset
):
    """Submits a request to CARROT's softwares find mapping"""
    # Create parameter list
    params = [
        ("software_id", software_id),
        ("name", name),
        ("description", description),
        ("repository_url", repository_url),
        ("created_by", created_by),
        ("created_before", created_before),
        ("created_after", created_after),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset)
    ]
    return request_handler.find("softwares", params)

def create(
    name,
    description,
    repository_url,
    created_by
):
    """Submits a request to CARROT's software create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
        ("repository_url", repository_url),
        ("created_by", created_by)
    ]
    return request_handler.create("softwares", params)

def update(
    software_id,
    name,
    description
):
    """Submits a request to CARROT's software update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
    ]
    return request_handler.update("softwares", software_id, params)

