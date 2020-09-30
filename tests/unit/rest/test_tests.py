import requests
import pytest
import mockito
import pprint

from carrot_cli.rest import request_handler, tests

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
                'description': 'This test will save Etheria',
                'test_input_defaults': {
                    "in_prev_owner": "Mara"
                },
                'eval_input_defaults': {
                    "in_creators": "Old Ones"
                },
                'name': 'Sword of Protection test',
                'template_id': '3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8',
                'test_id': 'cd987859-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "id":"3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "return":pprint.PrettyPrinter().pformat({
                "title": "No test found",
                "status": 404,
                "detail": "No test found with the specified ID"
            })
        }
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find_by_id('tests', request.param["id"]).thenReturn(request.param['return'])
    return request.param

def test_find_by_id(find_by_id_data):
    result = tests.find_by_id(find_by_id_data["id"])
    assert result == find_by_id_data["return"]

@pytest.fixture(
    params=[
        {
            "params":[
                ("test_id", ""),
                ("template_id", ""),
                ("name",'Queen of Bright Moon test'),
                ("template_name", ""),
                ("description", ""),
                ("test_input_defaults", ""),
                ("eval_input_defaults", ""),
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
                'description': 'This test leads the Rebellion',
                'test_input_defaults': {
                    "in_parent": "Angella"
                },
                'eval_input_defaults': {
                    "in_friend": "Bow"
                },
                'name': 'Queen of Bright Moon test',
                'template_id': '58723b05-6060-4444-9f1b-394aff691cce',
                'test_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}]
            )
        },
        {
            "params":[
                ("test_id","3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("template_id", ""),
                ("name",''),
                ("template_name", ""),
                ("description", ""),
                ("test_input_defaults", ""),
                ("eval_input_defaults", ""),
                ("created_by", ""),
                ("created_before", ""),
                ("created_after",""),
                ("sort", ""),
                ("limit", ""),
                ("offset", "")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "No tests found",
                "status": 404,
                "detail": "No tests found with the specified parameters"
            })
        }
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find('tests', request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_find(find_data):
    result = tests.find(
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
                ("name",'Horde Emperor test'),
                ("template_id","9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("description", "This test rules the known universe"),
                ("test_input_defaults", {
                    "in_nemesis": "She-Ra"
                }),
                ("eval_input_defaults", {
                    "in_brother": "Hordak"
                }),
                ("created_by", "hordeprime@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat(
                {'created_at': '2020-09-16T18:48:08.371563',
                'created_by': 'hordeprime@example.com',
                'test_input_defaults': {
                    "in_nemesis": "She-Ra"
                },
                'eval_input_defaults': {
                    "in_brother": "Hordak"
                },
                'description': 'This test rules the known universe',
                'name': 'Horde Emperor test',
                'template_id': '9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8',
                'test_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "params":[
                ("name",'Horde Emperor test'),
                ("template_id","9d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("description", "This test rules the known universe"),
                ("test_input_defaults", {
                    "in_nemesis": "She-Ra"
                }),
                ("eval_input_defaults", {
                    "in_brother": "Hordak"
                }),
                ("created_by", "hordeprime@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "Server error",
                "status": 500,
                "detail": "Error while attempting to insert new test"
            })
        }
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).create(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).create('tests', request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_create(create_data):
    result = tests.create(
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
                ("name",'Catra test'),
                ("description", "This test is trying to learn to process anger better")
            ],
            "return":pprint.PrettyPrinter().pformat(
                {'created_at': '2020-09-16T18:48:08.371563',
                'created_by': 'catra@example.com',
                'test_input_defaults': {
                    "in_nemesis?": "She-Ra"
                },
                'eval_input_defaults': {
                    "in_mother_figure": "Shadow Weaver"
                },
                'description': 'This test is trying to learn to process anger better',
                'name': 'Catra test',
                'template_id':'98536487-06fe-4b1a-9e96-47d4f36bf819',
                'test_id': 'bd132568-06fe-4b1a-9e96-47d4f36bf819'}
            )
        },
        {
            "id":"98536487-06fe-4b1a-9e96-47d4f36bf819",
            "params":[
                ("name",'Angella test'),
                ("description", "")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "Server error",
                "status": 500,
                "detail": "Error while attempting to update test"
            })
        }
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).update('tests', request.param["id"], request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_update(update_data):
    result = tests.update(
        update_data["id"],
        update_data["params"][0][1],
        update_data["params"][1][1],
    )
    assert result == update_data["return"]

@pytest.fixture(
    params=[
        {
            "id":"c97c25e5-4adf-4db7-8f64-19af34d84ef8",
            "params":[
                ("name",'King of Bright Moon run'),
                ("test_input", {
                    "in_daughter": "Glimmer"
                }),
                ("eval_input", {
                    "in_wife": "Angella"
                }),
                ("created_by", "micah@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "run_id": "69717609-0e95-4c9c-965c-1ea40a2cf44f",
                "test_id": "c97c25e5-4adf-4db7-8f64-19af34d84ef8",
                "name": "King of Bright Moon run",
                "status": "submitted",
                "test_input": {
                    "in_daughter": "Glimmer"
                },
                "eval_input": {
                    "in_wife": "Angella"
                },
                "cromwell_job_id": "f95ff110-88bd-4473-a5e1-dc7d5fc48d3a",
                "created_at": "2020-09-24T15:50:49.641333",
                "created_by": "micah@example.com",
                "finished_at": None
            })
        },
        {
            "id":"c97c25e5-4adf-4db7-8f64-19af34d84ef8",
            "params":[
                ("name",'Meditation run'),
                ("test_input", {
                    "occupation": "Princess"
                }),
                ("eval_input", {
                    "likes": "Plants, Mindfulness"
                }),
                ("created_by", "perfuma@example.com")
            ],
            "return":pprint.PrettyPrinter().pformat({
                "title": "Server error",
                "status": 500,
                "detail": "Error while attempting to query the database: NotFound"
            })
        }
    ]
)
def run_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).run(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).run(request.param["id"], request.param["params"]).thenReturn(request.param['return'])
    return request.param

def test_run(run_data):
    result = tests.run(
        run_data["id"],
        run_data["params"][0][1],
        run_data["params"][1][1],
        run_data["params"][2][1],
        run_data["params"][3][1],
    )
    assert result == run_data["return"]

@pytest.fixture(
    params=[
        {
            "id":"047e27ad-2890-4372-b2cb-dfec57347eb9",
            "email":"bow@example.com",
            "return":pprint.PrettyPrinter().pformat({
                "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                "entity_type": "test",
                "entity_id": "047e27ad-2890-4372-b2cb-dfec57347eb9",
                "email": "bow@example.com",
                "created_at": "2020-09-23T19:41:46.839880"
            })
        },
        {
            "id":"98536487-06fe-4b1a-9e96-47d4f36bf819",
            "email":"huntara@example.com",
            "return":pprint.PrettyPrinter().pformat({
                "title": "No test found",
                "status": 404,
                "detail": "No test found with the specified ID"
            })
        }
    ]
)
def subscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).subscribe('tests', request.param["id"], request.param["email"]).thenReturn(request.param['return'])
    return request.param

def test_subscribe(subscribe_data):
    result = tests.subscribe(
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
    mockito.when(request_handler).unsubscribe('tests', request.param["id"], request.param["email"]).thenReturn(request.param['return'])
    return request.param

def test_unsubscribe(unsubscribe_data):
    result = tests.unsubscribe(
        unsubscribe_data["id"],
        unsubscribe_data["email"],
    )
    assert result == unsubscribe_data["return"]