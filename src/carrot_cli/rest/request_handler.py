import logging
import pprint
import requests
from ..config import manager as config

LOGGER = logging.getLogger(__name__)

def find_by_id(entity, id):
    """Submits a request to the find_by_id mapping for the specified entity with the specified id"""
    # Build request address and send
    address = "http://%s/api/v1/%s/%s" % (config.load_var("carrot_server_address"), entity, id)
    req = requests.Request('GET', address)
    return send_request(req)

def find(entity, params):
    """Submits a request to the find mapping for the specified entity with the specified params"""
    #Build request address
    address = "http://%s/api/v1/%s" % (config.load_var("carrot_server_address"), entity)
    # Filter out params that are not set
    params = list(filter(lambda param: param[1] != "", params))
    # Create and send request
    req = requests.Request('GET', address, params=params)
    return send_request(req)

def create(entity, params):
    """Submits a request to create mapping for the specified entity with the specified params"""
    # Build request address
    address = "http://%s/api/v1/%s" % (config.load_var("carrot_server_address"), entity)
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    req = requests.Request("POST", address, json=body)
    return send_request(req)

def update(entity, id, params):
    """
        Submits a request to update mapping for the specified entity with the specified id and 
        params
    """
    # Build request address
    address = "http://%s/api/v1/%s/%s" % (config.load_var("carrot_server_address"), entity, id)
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    req = requests.Request("PUT", address, json=body)
    return send_request(req)

def subscribe(entity, id, email):
    """
        Submits a request to the subscribe mapping for the specified entity with the specified id 
        and email
    """
    # Build request address
    address = "http://%s/api/v1/%s/%s/subscriptions" % (config.load_var("carrot_server_address"), 
        entity, id)
    # Build request json body with email
    body = {"email": email}
    # Build and send request
    req = requests.Request("POST", address, json=body)
    return send_request(req)

def unsubscribe(entity, id, email):
    """
        Submits a request to the subscribe mapping for the specified entity with the specified id 
        and email
    """
    # Build request address
    address = "http://%s/api/v1/%s/%s/subscriptions" % (config.load_var("carrot_server_address"), 
        entity, id)
    # Build request json body with email
    body = {"email": email}
    # Build and send request
    req = requests.Request("DELETE", address, json=body)
    return send_request(req)

def run(test_id, params):
    """
        Submits a POST request to the run mapping for the test with the specified id and params
    """
    # Build request address
    address = "http://%s/api/v1/tests/%s/runs" % (config.load_var("carrot_server_address"), 
        test_id)
    # Build request json body from params, filtering out empty ones
    body = {}
    for param in params:
        if param[1] != "":
            body[param[0]] = param[1]
    # Build and send request
    req = requests.Request("POST", address, json=body)
    return send_request(req)

def send_request(req):
    """Sends the specified Request object and handles potential errors"""
    try:
        # Prepare and send request
        prep_req = req.prepare()
        LOGGER.debug("Sending %s request to %s", prep_req.method, prep_req.url)
        sesh = requests.Session()
        response = sesh.send(prep_req)
        LOGGER.debug(
            "Received response with status %i and body %s",
            response.status_code,
            response.text
        )
        # Parse json body from request and return
        return pprint.PrettyPrinter().pformat(response.json())
    except ValueError:
        LOGGER.debug("Failed to parse json from response body: %s", response.text)
        return response.text
    except requests.ConnectionError as err:
        LOGGER.debug(err)
        return "Encountered a connection error. Enable verbose logging (-v) for more info"
    except requests.URLRequired as err:
        LOGGER.debug(err)
        return "Invalid URL. Enable verbose logging (-v) for more info"
    except requests.Timeout as err:
        LOGGER.debug(err)
        return "Request timed out. Enable verbose logging (-v) for more info"
    except requests.TooManyRedirects as err:
        LOGGER.debug(err)
        return "Too many redirects. Enable verbose logging (-v) for more info"
