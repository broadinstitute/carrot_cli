import logging

from . import request_handler

LOGGER = logging.getLogger(__name__)


def create_map(report_id, section_id, name, position, created_by):
    """Submits a request to CARROT's report_section create mapping"""
    return request_handler.create_map(
        "reports",
        report_id,
        "sections",
        section_id,
        [("name", name), ("position", position), ("created_by", created_by)],
    )


def find_maps(
    report_id,
    section_id,
    name,
    position,
    created_before,
    created_after,
    created_by,
    sort,
    limit,
    offset,
):
    """Submits a request to CARROT's report_section find mapping"""
    # Create parameter list
    params = [
        ("section_id", section_id),
        ("name", name),
        ("position", position),
        ("created_before", created_before),
        ("created_after", created_after),
        ("created_by", created_by),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset),
    ]
    return request_handler.find_maps("reports", report_id, "sections", params)


def find_map_by_ids_and_name(report_id, section_id, name):
    """Submits a request to CARROT's report_section find_by_ids_and_name mapping"""
    return request_handler.find_map_by_ids_and_name(
        "reports", report_id, "sections", section_id, name
    )

def delete_map_by_ids_and_name(report_id, section_id, name):
    """Submits a request to CARROT's report_section delete mapping"""
    return request_handler.delete_map_by_ids_and_name(
        "reports", report_id, "sections", section_id, name
    )
