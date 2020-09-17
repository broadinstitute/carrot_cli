import logging
from . import request_handler

LOGGER = logging.getLogger(__name__)

def find_by_id(test_id):
    """Submits a request to CARROT's tests find_by_id mapping"""
    return request_handler.find_by_id("tests", test_id)

def find(
    test_id,
    template_id,
    name,
    template_name,
    description,
    test_input_defaults,
    eval_input_defaults,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset
):
    """Submits a request to CARROT's tests find mapping"""
    # Create parameter list
    params = [
        ("test_id", test_id),
        ("template_id", template_id),
        ("name", name),
        ("template_name", template_name),
        ("description", description),
        ("test_input_defaults", test_input_defaults),
        ("eval_input_defaults", eval_input_defaults),
        ("created_by", created_by),
        ("created_before", created_before),
        ("created_after", created_after),
        ("sort", sort),
        ("limit", limit),
        ("offset", offset)
    ]
    return request_handler.find("tests", params)

def create(
    name,
    template_id,
    description,
    test_input_defaults,
    eval_input_defaults,
    created_by
):
    """Submits a request to CARROT's tests create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("template_id", template_id),
        ("description", description),
        ("test_input_defaults", test_input_defaults),
        ("eval_input_defaults", eval_input_defaults),
        ("created_by", created_by)
    ]
    return request_handler.create("tests", params)

def update(
    test_id,
    name,
    description
):
    """Submits a request to CARROT's tests update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
    ]
    return request_handler.update("tests", test_id, params)

def run(
    test_id,
    name,
    test_input,
    eval_input,
    created_by
):
    """Submits a request to CARROT's test run mapping"""
    # Load data from files for test_input and eval_input, if set
    if test_input != "":
        with open(test_input, 'r') as test_input_file:
            test_input = test_input_file.read()
    if eval_input != "":
        with open(eval_input, 'r') as eval_input_file:
            eval_input = eval_input_file.read()
    # Create parameter list
    params = [
        ("name", name),
        ("test_input", test_input),
        ("eval_input", eval_input),
        ("created_by", created_by)
    ]
    return request_handler.run(test_id, params)


def subscribe(
    test_id,
    email
):
    """Submits a request to CARROT's tests subscribe mapping"""
    return request_handler.subscribe("tests", test_id, email)

def unsubscribe(
    test_id,
    email
):
    """Submits a request to CARROT's tests unsubscribe mapping"""
    return request_handler.unsubscribe("tests", test_id, email)
