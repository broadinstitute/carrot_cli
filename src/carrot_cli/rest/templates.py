import logging

from . import request_handler

LOGGER = logging.getLogger(__name__)


def find_by_id(template_id):
    """Submits a request to CARROT's templates find_by_id mapping"""
    return request_handler.find_by_id("templates", template_id)


def find(
    template_id="",
    pipeline_id="",
    name="",
    description="",
    test_wdl="",
    eval_wdl="",
    created_by="",
    created_before="",
    created_after="",
    sort="",
    limit="",
    offset="",
):
    """Submits a request to CARROT's templates find mapping"""
    # Create parameter list
    params = [
        ("template_id", template_id),
        ("pipeline_id", pipeline_id),
        ("name", name),
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


def create(
    name,
    pipeline_id,
    description,
    test_wdl,
    test_wdl_dependencies,
    eval_wdl,
    eval_wdl_dependencies,
    created_by
):
    """Submits a request to CARROT's templates create mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("pipeline_id", pipeline_id),
        ("description", description),
        ("created_by", created_by),
    ]
    # Start files as an empty dict
    files = {}
    # Process test and eval wdls and dependen cies to put them in the correct lists depending on
    # how they are provided
    wdl_error = __process_wdl(params, files, test_wdl, "test")
    if test_wdl_dependencies:
        wdl_error = wdl_error if wdl_error else __process_wdl_dependencies(params, files, test_wdl_dependencies, "test")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    wdl_error = wdl_error if wdl_error else __process_wdl(params, files, eval_wdl, "eval")
    if eval_wdl_dependencies:
        wdl_error = wdl_error if wdl_error else __process_wdl_dependencies(params, files, eval_wdl_dependencies, "eval")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    # If there was an error, return it
    if wdl_error:
        return wdl_error
    # Make the request
    return request_handler.create("templates", params, files=(files if files else None))


def update(
    template_id,
    name,
    description,
    test_wdl,
    test_wdl_dependencies,
    eval_wdl,
    eval_wdl_dependencies
):
    """Submits a request to CARROT's templates update mapping"""
    # Create parameter list
    params = [
        ("name", name),
        ("description", description),
    ]
    # Start files as an empty dict
    files = {}
    # Process test and eval wdls and dependencies (if provided) to put them in the correct lists
    # depending on how they are provided
    if test_wdl:
        wdl_error = __process_wdl(params, files, test_wdl, "test")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    if test_wdl_dependencies:
        wdl_error = __process_wdl_dependencies(params, files, test_wdl_dependencies, "test")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    if eval_wdl:
        wdl_error = __process_wdl(params, files, eval_wdl, "eval")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    if eval_wdl_dependencies:
        wdl_error = __process_wdl_dependencies(params, files, eval_wdl_dependencies, "eval")
        # If there was an error, return it
        if wdl_error:
            return wdl_error
    # Make the request
    return request_handler.update("templates", template_id, params, files=(files if files else None))


def delete(template_id):
    """Submits a request to CARROT's templates delete mapping"""
    return request_handler.delete("templates", template_id)


def subscribe(template_id, email):
    """Submits a request to CARROT's templates subscribe mapping"""
    return request_handler.subscribe("templates", template_id, email)


def unsubscribe(template_id, email):
    """Submits a request to CARROT's templates unsubscribe mapping"""
    return request_handler.unsubscribe("templates", template_id, email)


def __process_wdl(params, files, wdl, type):
    # If wdl is an http or gs uri, we'll add it to params
    if wdl.startswith("http://") or wdl.startswith("https://") or wdl.startswith("gs://"):
        params.append((f"{type}_wdl", wdl))
    # Otherwise, assume wdl is a file, so we'll try to open it and put it in a files list
    else:
        try:
            wdl_file = open(wdl, "rt")
            files[f'{type}_wdl_file'] = (f'{type}.wdl', wdl_file)
        except IOError as e:
            LOGGER.debug(e)
            if LOGGER.getEffectiveLevel() == logging.DEBUG:
                return f"Failed to open {type} wdl file with path {wdl}."
            else:
                return f"Failed to open {type} wdl file with path {wdl}. Enable verbose logging (-v) for more info"
    # Return None if all goes well
    return None

def __process_wdl_dependencies(params, files, wdl_dependencies, type):
    # If wdl is an http or gs uri, we'll add it to params
    if wdl_dependencies.startswith("http://")\
            or wdl_dependencies.startswith("https://")\
            or wdl_dependencies.startswith("gs://"):
        params.append((f"{type}_wdl_dependencies", wdl_dependencies))
    # Otherwise, assume wdl_dependencies is a file, so we'll try to open it and put it in a files list
    else:
        try:
            wdl_file = open(wdl_dependencies, "rb")
            files[f'{type}_wdl_dependencies_file'] = (f'{type}_dependencies.zip', wdl_file)
        except IOError as e:
            LOGGER.debug(e)
            if LOGGER.getEffectiveLevel() == logging.DEBUG:
                return f"Failed to open {type} wdl dependencies file with path {wdl_dependencies}."
            else:
                return f"Failed to open {type} wdl dependencies file with path {wdl_dependencies}. " \
                       f"Enable verbose logging (-v) for more info"
    # Return None if all goes well
    return None