import logging

from . import request_handler

LOGGER = logging.getLogger(__name__)


def find_by_id(report_id):
    """Submits a request to CARROT's reports find_by_id mapping"""
    return request_handler.find_by_id("reports", report_id)


def find(
    report_id,
    name,
    description,
    metadata,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Submits a request to CARROT's reports find mapping"""
    # Create parameter list
    params = [
        ("report_id", report_id),
        ("name", name),
        ("description", description),
        ("metadata", metadata),
        ("created_by", created_by),
        ("created_before", created_before),
        ("created_after", created_after),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset),
    ]
    return request_handler.find("reports", params)


def create(name, description, created_by):
    """Submits a request to CARROT's reports create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
        ("created_by", created_by)
    ]
    return request_handler.create("reports", params)


def update(report_id, name, description):
    """Submits a request to CARROT's reports update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
    ]
    return request_handler.update("reports", report_id, params)

def delete(report_id):
    """Submits a request to CARROT's reports delete mapping"""
    return request_handler.delete("reports", report_id)
