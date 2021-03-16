import logging

from . import request_handler

LOGGER = logging.getLogger(__name__)


def find_by_id(section_id):
    """Submits a request to CARROT's sections find_by_id mapping"""
    return request_handler.find_by_id("sections", section_id)


def find(
    section_id,
    name,
    description,
    contents,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Submits a request to CARROT's sections find mapping"""
    # Create parameter list
    params = [
        ("section_id", section_id),
        ("name", name),
        ("description", description),
        ("contents", contents),
        ("created_by", created_by),
        ("created_before", created_before),
        ("created_after", created_after),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset),
    ]
    return request_handler.find("sections", params)


def create(name, description, contents, created_by):
    """Submits a request to CARROT's sections create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
        ("contents", contents),
        ("created_by", created_by)
    ]
    return request_handler.create("sections", params)


def update(section_id, name, description, contents):
    """Submits a request to CARROT's sections update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
        ("contents", contents),
    ]
    return request_handler.update("sections", section_id, params)

def delete(section_id):
    """Submits a request to CARROT's sections delete mapping"""
    return request_handler.delete("sections", section_id)
