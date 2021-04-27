import logging

from . import request_handler

LOGGER = logging.getLogger(__name__)


def find_by_id(template_id):
    """Submits a request to CARROT's templates find_by_id mapping"""
    return request_handler.find_by_id("templates", template_id)


def find(
    template_id,
    pipeline_id,
    name,
    pipeline_name,
    description,
    test_wdl,
    eval_wdl,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Submits a request to CARROT's templates find mapping"""
    # Create parameter list
    params = [
        ("template_id", template_id),
        ("pipeline_id", pipeline_id),
        ("name", name),
        ("pipeline_name", pipeline_name),
        ("description", description),
        ("test_wdl", test_wdl),
        ("eval_wdl", eval_wdl),
        ("created_by", created_by),
        ("created_before", created_before),
        ("created_after", created_after),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset),
    ]
    return request_handler.find("templates", params)


def create(name, pipeline_id, description, test_wdl, eval_wdl, created_by):
    """Submits a request to CARROT's templates create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("pipeline_id", pipeline_id),
        ("description", description),
        ("test_wdl", test_wdl),
        ("eval_wdl", eval_wdl),
        ("created_by", created_by),
    ]
    return request_handler.create("templates", params)


def update(template_id, name, description, test_wdl, eval_wdl):
    """Submits a request to CARROT's templates update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
        ("test_wdl", test_wdl),
        ("eval_wdl", eval_wdl),
    ]
    return request_handler.update("templates", template_id, params)


def delete(template_id):
    """Submits a request to CARROT's templates delete mapping"""
    return request_handler.delete("templates", template_id)


def subscribe(template_id, email):
    """Submits a request to CARROT's templates subscribe mapping"""
    return request_handler.subscribe("templates", template_id, email)


def unsubscribe(template_id, email):
    """Submits a request to CARROT's templates unsubscribe mapping"""
    return request_handler.unsubscribe("templates", template_id, email)
