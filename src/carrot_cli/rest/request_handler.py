import json as json_lib
import logging
import pprint
import urllib

import requests

from ..config import manager as config

LOGGER = logging.getLogger(__name__)


def find_by_id(entity, id):
    """Submits a request to the find_by_id mapping for the specified entity with the specified id"""
    # Build request address and send
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}"
    return send_request("GET", address)


def find(entity, params):
    """Submits a request to the find mapping for the specified entity with the specified params"""
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}"
    # Filter out params that are not set
    params = list(filter(lambda param: param[1] != "", params))
    # Create and send request
    return send_request("GET", address, params=params)


def create(entity, params, files=None):
    """
    Submits a request to create mapping for the specified entity with the specified params.
    If a value is specified for files, the request body will be multipart/form-data. If not, the
    request will have a json body
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}"
    # Build request body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    # If we have files, send multipart
    if files:
        return send_request("POST", address, body=body, files=files)
    # Otherwise, send json
    else:
        return send_request("POST", address, json=body)


def update(entity, id, params, files=None):
    """
    Submits a request to update mapping for the specified entity with the specified id and
    params. If a value is specified for files, the request body will be multipart/form-data. If
    not, the request will have a json body
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}"
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    # If we have files, send multipart
    if files:
        return send_request("PUT", address, body=body, files=files)
    # Otherwise, send json
    else:
        return send_request("PUT", address, json=body)


def delete(entity, id):
    """
    Submits a request to the delete mapping for the specified entity with the specified id
    """
    # Build request address and send
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}"
    return send_request("DELETE", address)


def subscribe(entity, id, email):
    """
    Submits a request to the subscribe mapping for the specified entity with the specified id
    and email
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}/subscriptions"
    # Build request json body with email
    body = {"email": email}
    # Build and send request
    return send_request("POST", address, json=body)


def unsubscribe(entity, id, email):
    """
    Submits a request to the subscribe mapping for the specified entity with the specified id
    and email
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}/subscriptions"
    # Build request params with email
    params = [("email", email)]
    # Build and send request
    return send_request("DELETE", address, params=params)


def run(test_id, params):
    """
    Submits a POST request to the run mapping for the test with the specified id and params
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/tests/{test_id}/runs"
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    return send_request("POST", address, json=body)


def find_runs(entity, id, params):
    """
    Submits a request to the find_runs mapping for the specified entity with the specified id
    and filtering by the specified params
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity}/{id}/runs"
    # Filter out params that are not set
    params = list(filter(lambda param: param[1] != "", params))
    # Create and send request
    return send_request("GET", address, params=params)


def create_map(entity1, entity1_id, entity2, entity2_id, params, query_params=None):
    """
    Submits a request for creating a mapping between entity1 and entity2, with the specified
    params.
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = (
        f"http://{server_address}/api/v1/{entity1}/{entity1_id}/{entity2}/{entity2_id}"
    )
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Create and send request
    return send_request("POST", address, json=body, params=query_params)


def find_map_by_ids(entity1, entity1_id, entity2, entity2_id):
    """
    Submits a request for finding a mapping between entity1 and entity2, with the specified
    ids.
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = (
        f"http://{server_address}/api/v1/{entity1}/{entity1_id}/{entity2}/{entity2_id}"
    )
    # Create and send request
    return send_request("GET", address)


def find_maps(entity1, entity1_id, entity2, params):
    """
    Submits a request to the find_maps mapping for the specified entity with the specified id
    and filtering by the specified params
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = f"http://{server_address}/api/v1/{entity1}/{entity1_id}/{entity2}"
    # Filter out params that are not set
    params = list(filter(lambda param: param[1] != "", params))
    # Create and send request
    return send_request("GET", address, params=params)


def delete_map_by_ids(entity1, entity1_id, entity2, entity2_id):
    """
    Submits a request for deleting a mapping between entity1 and entity2, with the specified
    ids.
    """
    # Build request address
    server_address = config.load_var("carrot_server_address")
    address = (
        f"http://{server_address}/api/v1/{entity1}/{entity1_id}/{entity2}/{entity2_id}"
    )
    # Create and send request
    return send_request("DELETE", address)


def send_request(method, url, params=None, json=None, body=None, files=None):
    """
    Sends a request to url with method, optionally with query params, json, form data body, and
    files, and handles potential errors
    """
    try:
        # Send request
        LOGGER.debug(
            "Sending %s request to %s with params %s and body %s",
            method,
            url,
            params,
            json,
        )
        response = requests.request(method, url, params=params, json=json, data=body, files=files)
        LOGGER.debug(
            "Received response with status %i and body %s",
            response.status_code,
            response.text,
        )
        # Parse json body from request and return
        json_body = response.json()
        if json_body is None:
            return (
                "Received response with status %i and empty body" % response.status_code
            )
        return json_lib.dumps(json_body, indent=4, sort_keys=True)
    except (AttributeError, json_lib.decoder.JSONDecodeError):
        LOGGER.debug("Failed to parse json from response body: %s", response.text)
        return json_lib.dumps(
            {"Status": response.status_code, "Body": response.text},
            indent=4,
            sort_keys=True,
        )
    except requests.ConnectionError as err:
        LOGGER.debug(err)
        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            return "Encountered a connection error."
        else:
            return "Encountered a connection error. Enable verbose logging (-v) for more info"
    except requests.URLRequired as err:
        LOGGER.debug(err)
        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            return "Invalid URL."
        else:
            return "Invalid URL. Enable verbose logging (-v) for more info"
    except requests.Timeout as err:
        LOGGER.debug(err)
        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            return "Request timed out."
        else:
            return "Request timed out. Enable verbose logging (-v) for more info"
    except requests.TooManyRedirects as err:
        LOGGER.debug(err)
        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            return "Too many redirects"
        else:
            return "Too many redirects. Enable verbose logging (-v) for more info"
