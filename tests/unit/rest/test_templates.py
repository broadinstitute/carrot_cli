import requests
import pytest
import mockito
import pprint

from carrot_cli.rest import request_handler, templates

@pytest.fixture(autouse=True)
def unstub():
    yield
    mockito.unstub()

@pytest.fixture(
    params=[
        {
            "id":"cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "return":pprint.PrettyPrinter().pformat(
                {'created_at': '2020-09-16T18:48:06.371563',
                'created_by': 'adora@example.com',
                'description': 'This template will save Etheria',
                'test_wdl': 'example.com/she-ra_test.wdl',
                'eval_wdl': 'example.com/she-ra_eval.wdl',
                'name': 'Sword of Protection template',
                'pipeline_id': '3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8',
                'template_id': 'cd987859-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "id":"3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "return":pprint.PrettyPrinter().pformat({
                "title": "No template found",
                "status": 404,
                "detail": "No template found with the specified ID"
            })
        }
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find_by_id('templates', request.param["id"]).thenReturn(request.param['return'])
    return request.param

def test_find_by_id(find_by_id_data):
    result = templates.find_by_id(find_by_id_data["id"])
    assert result == find_by_id_data["return"]

@pytest.fixture(
    params=[
        {
            "params":[
                ("template_id", ""),
                ("pipeline_id", ""),
                ("name",'Queen of Bright Moon template'),
                ("pipeline_name", ""),
                ("description", ""),
                ("test_wdl", ""),
                ("eval_wdl", ""),
                ("created_by", ""),
                ("created_before", ""),
                ("created_after",""),
                ("sort", ""),
                ("limit", ""),
                ("offset", "")
            ],
            "return":pprint.PrettyPrinter().pformat(
                [{'created_at': '2020-09-16T18:48:08.371563',
                'created_by': 'glimmer@example.com',
                'description': 'This template leads the Rebellion',
                'test_wdl': 'example.com/etheria_test.wdl',
                'eval_wdl': 'example.com/etheria_eval.wdl',
                'name': 'Queen of Bright Moon template',
                'pipeline_id': '58723b05-6060-4444-9f1b-394aff691cce',
                'template_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}]
            )
        },
        {
            "params":[
                ("template_id","3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("pipeline_id", ""),
                ("name",''),
                ("pipeline_name", ""),
                ("description", ""),
                ("test_wdl", ""),
                ("eval_wdl", ""),
                ("created_by", ""),
                ("created_before", ""),
                ("created_after",""),
                ("sort", ""),
                ("limit", ""),
                ("offset", "")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "No templates found",
                "status": 404,
                "detail": "No templates found with the specified parameters"
            })
        }
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find('templates', request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_find(find_data):
    result = templates.find(
        find_data["params"][0][1],
        find_data["params"][1][1],
        find_data["params"][2][1],
        find_data["params"][3][1],
        find_data["params"][4][1],
        find_data["params"][5][1],
        find_data["params"][6][1],
        find_data["params"][7][1],
        find_data["params"][8][1],
        find_data["params"][9][1],
        find_data["params"][10][1],
        find_data["params"][11][1],
        find_data["params"][12][1],

    )
    assert result == find_data["return"]

@pytest.fixture(
    params=[
        {
            "params":[
                ("name",'Horde Emperor template'),
                ("pipeline_id","9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("description", "This template rules the known universe"),
                ("test_wdl", "example.com/horde_test.wdl"),
                ("eval_wdl", "example.com/horde_eval.wdl"),
                ("created_by", "hordeprime@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat(
                {'created_at': '2020-09-16T18:48:08.371563',
                'created_by': 'hordeprime@example.com',
                'test_wdl': 'example.com/horde_test.wdl',
                'eval_wdl': 'example.com/horde_eval.wdl',
                'description': 'This template rules the known universe',
                'name': 'Horde Emperor template',
                'pipeline_id': '9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8',
                'template_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "params":[
                ("name",'Horde Emperor template'),
                ("pipeline_id","9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("description", "This template rules the known universe"),
                ("test_wdl", "example.com/horde_test.wdl"),
                ("eval_wdl", "example.com/horde_eval.wdl"),
                ("created_by", "hordeprime@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "Server error",
                "status": 500,
                "detail": "Error while attempting to insert new template"
            })
        }
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).create(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).create('templates', request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_create(create_data):
    result = templates.create(
        create_data["params"][0][1],
        create_data["params"][1][1],
        create_data["params"][2][1],
        create_data["params"][3][1],
        create_data["params"][4][1],
        create_data["params"][5][1],
    )
    assert result == create_data["return"]

@pytest.fixture(
    params=[
        {
            "id":"bd132568-06fe-4b1a-9e96-47d4f36bf819",
            "params":[
                ("name",'Catra template'),
                ("description", "This template is trying to learn to process anger better")
            ],
            "return":pprint.PrettyPrinter().pformat(
                {'created_at': '2020-09-16T18:48:08.371563',
                'created_by': 'catra@example.com',
                "test_wdl": "example.com/horde_test.wdl",
                "eval_wdl": "example.com/horde_eval.wdl",
                'description': 'This template is trying to learn to process anger better',
                'name': 'Catra template',
                'pipeline_id':'98536487-06fe-4b1a-9e96-47d4f36bf819',
                'template_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "id":"98536487-06fe-4b1a-9e96-47d4f36bf819",
            "params":[
                ("name",'Angella template'),
                ("description", "")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "Server error",
                "status": 500,
                "detail": "Error while attempting to update new template"
            })
        }
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).update('templates', request.param["id"], request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_update(update_data):
    result = templates.update(
        update_data["id"],
        update_data["params"][0][1],
        update_data["params"][1][1],
    )
    assert result == update_data["return"]

@pytest.fixture(
    params=[
        {
            "id":"047e27ad-2890-4372-b2cb-dfec57347eb9",
            "email":"bow@example.com",
            "return":pprint.PrettyPrinter().pformat({
                "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                "entity_type": "template",
                "entity_id": "047e27ad-2890-4372-b2cb-dfec57347eb9",
                "email": "bow@example.com",
                "created_at": "2020-09-23T19:41:46.839880"
            })
        },
        {
            "id":"98536487-06fe-4b1a-9e96-47d4f36bf819",
            "email":"huntara@example.com",
            "return":pprint.PrettyPrinter().pformat({
                "title": "No template found",
                "status": 404,
                "detail": "No template found with the specified ID"
            })
        }
    ]
)
def subscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).subscribe('templates', request.param["id"], request.param["email"]).thenReturn(request.param['return'])
    return request.param

def test_subscribe(subscribe_data):
    result = templates.subscribe(
        subscribe_data["id"],
        subscribe_data["email"],
    )
    assert result == subscribe_data["return"]

@pytest.fixture(
    params=[
        {
            "id":"047e27ad-2890-4372-b2cb-dfec57347eb9",
            "email":"mermista@example.com",
            "return":pprint.PrettyPrinter().pformat(
                {'message': 'Successfully deleted 1 row(s)'}
            )
        },
        {
            "id":"98536487-06fe-4b1a-9e96-47d4f36bf819",
            "email":"castaspella@example.com",
            "return":pprint.PrettyPrinter().pformat({
                "title": "No subscription found",
                "status": 404,
                "detail": "No subscription found for the specified parameters"
            })
        }
    ]
)
def unsubscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).unsubscribe('templates', request.param["id"], request.param["email"]).thenReturn(request.param['return'])
    return request.param

def test_unsubscribe(unsubscribe_data):
    result = templates.unsubscribe(
        unsubscribe_data["id"],
        unsubscribe_data["email"],
    )
    assert result == unsubscribe_data["return"]