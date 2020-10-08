import pprint

import mockito
import pytest
from click.testing import CliRunner

from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.config import manager as config
from carrot_cli.rest import runs, tests


@pytest.fixture(autouse=True)
def unstub():
    yield
    mockito.unstub()

@pytest.fixture(autouse=True)
def no_email():
    mockito.when(config).load_var_no_error("email").thenReturn(None)

@pytest.fixture(
    params=[
        {
            "args": ["test", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This test will save Etheria",
                    "test_input_defaults": {"in_greeted": "Cool Person"},
                    "eval_input_defaults": {"in_output_filename": "test_greeting.txt"},
                    "name": "Sword of Protection test",
                    "template_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "test_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["test", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No test found",
                    "status": 404,
                    "detail": "No test found with the specified ID",
                }
            ),
        },
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(tests).find_by_id(request.param["args"][2]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_find_by_id(find_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_by_id_data["args"])
    assert result.output == find_by_id_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "find",
                "--test_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--template_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection test",
                "--template_name",
                "Sword of Protection template",
                "--description",
                "This test will save Etheria",
                "--test_input_defaults",
                "tests/data/mock_test_input.json",
                "--eval_input_defaults",
                "tests/data/mock_eval_input.json",
                "--created_by",
                "adora@example.com",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(name)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "Sword of Protection test",
                "Sword of Protection template",
                "This test will save Etheria",
                '{"in_greeted": "Cool Person"}\n',
                '{"in_output_filename": "test_greeting.txt"}\n',
                "adora@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(name)",
                1,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                [
                    {
                        "created_at": "2020-09-16T18:48:06.371563",
                        "created_by": "adora@example.com",
                        "description": "This test will save Etheria",
                        "test_input_defaults": {"in_greeted": "Cool Person"},
                        "eval_input_defaults": {
                            "in_output_filename": "test_greeting.txt"
                        },
                        "name": "Sword of Protection test",
                        "template_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "test_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ]
            ),
        },
        {
            "args": [
                "test",
                "find",
                "--test_id",
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
            ],
            "params": [
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                20,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No tests found",
                    "status": 404,
                    "detail": "No tests found with the specified parameters",
                }
            ),
        },
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(tests).find(
        request.param["params"][0],
        request.param["params"][1],
        request.param["params"][2],
        request.param["params"][3],
        request.param["params"][4],
        request.param["params"][5],
        request.param["params"][6],
        request.param["params"][7],
        request.param["params"][8],
        request.param["params"][9],
        request.param["params"][10],
        request.param["params"][11],
        request.param["params"][12],
    ).thenReturn(request.param["return"])
    return request.param


def test_find(find_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_data["args"])
    assert result.output == find_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "create",
                "--template_id",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection test",
                "--description",
                "This test will save Etheria",
                "--test_input_defaults",
                "tests/data/mock_test_input.json",
                "--eval_input_defaults",
                "tests/data/mock_eval_input.json",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "Sword of Protection test",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "This test will save Etheria",
                '{"in_greeted": "Cool Person"}\n',
                '{"in_output_filename": "test_greeting.txt"}\n',
                "adora@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This test will save Etheria",
                    "test_input_defaults": {"in_greeted": "Cool Person"},
                    "eval_input_defaults": {"in_output_filename": "test_greeting.txt"},
                    "name": "Sword of Protection test",
                    "template_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "test_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": [
                "test",
                "create",
                "--template_id",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection test",
                "--description",
                "This test will save Etheria",
                "--test_input_defaults",
                "tests/data/mock_test_input.json",
                "--eval_input_defaults",
                "tests/data/mock_eval_input.json",
            ],
            "params": [],
            "return": "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
        },
        {
            "args": ["test", "create"],
            "params": [],
            "return": "Usage: carrot_cli test create [OPTIONS]\n"
            "Try 'carrot_cli test create --help' for help.\n"
            "\n"
            "Error: Missing option '--name'.",
        },
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).create(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(tests).create(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
            request.param["params"][5],
        ).thenReturn(request.param["return"])
    return request.param


def test_create(create_data):
    runner = CliRunner()
    result = runner.invoke(carrot, create_data["args"])
    assert result.output == create_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "update",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--description",
                "This new test replaced the broken one",
                "--name",
                "New Sword of Protection test",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "New Sword of Protection test",
                "This new test replaced the broken one",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This test replaced the broken one",
                    "test_input_defaults": {"in_greeted": "Cool Person"},
                    "eval_input_defaults": {"in_output_filename": "test_greeting.txt"},
                    "name": "New Sword of Protection test",
                    "template_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "test_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["test", "update"],
            "params": [],
            "return": "Usage: carrot_cli test update [OPTIONS] ID\n"
            "Try 'carrot_cli test update --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).update(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(tests).update(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
        ).thenReturn(request.param["return"])
    return request.param


def test_update(update_data):
    runner = CliRunner()
    result = runner.invoke(carrot, update_data["args"])
    assert result.output == update_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "run",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Queen of Bright Moon run",
                "--test_input",
                "tests/data/mock_test_input.json",
                "--eval_input",
                "tests/data/mock_eval_input.json",
                "--created_by",
                "glimmer@example.com",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "Queen of Bright Moon run",
                '{"in_greeted": "Cool Person"}\n',
                '{"in_output_filename": "test_greeting.txt"}\n',
                "glimmer@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                [
                    {
                        "created_at": "2020-09-16T18:48:06.371563",
                        "finished_at": "2020-09-16T18:58:06.371563",
                        "created_by": "glimmer@example.com",
                        "test_input": {"in_mother": "Angella"},
                        "eval_input": {"in_friend": "Bow"},
                        "status": "succeeded",
                        "results": {},
                        "cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                        "name": "Queen of Bright Moon run",
                        "test_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ]
            ),
        },
        {
            "args": [
                "test", 
                "run", 
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "--created_by",
                "frosta@example.com",
            ],
            "params": [
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "",
                "",
                "",
                "frosta@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "detail": "Error while attempting to query the database: NotFound",
                    "status": 500,
                    "title": "Server error",
                }
            ),
        },
        {
            "args": [
                "test",
                "run",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Queen of Bright Moon run",
                "--test_input",
                "tests/data/mock_test_input.json",
                "--eval_input",
                "tests/data/mock_eval_input.json",
            ],
            "params": [],
            "return": "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
        },
        {
            "args": [
                "test",
                "run",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Queen of Bright Moon run",
                "--test_input",
                "nonexistent_file.json",
                "--eval_input",
                "tests/data/mock_eval_input.json",
                "--created_by",
                "glimmer@example.com",
            ],
            "params": [],
            "return": "Failed to locate file with name nonexistent_file.json",
        },
    ]
)
def run_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).run(...).thenReturn(None)
    # Mock up request response
    if len(request.param["params"]) > 0:
        mockito.when(tests).run(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
        ).thenReturn(request.param["return"])
    return request.param


def test_run(run_data):
    runner = CliRunner()
    result = runner.invoke(carrot, run_data["args"])
    assert result.output == run_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "find_runs",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Queen of Bright Moon run",
                "--status",
                "succeeded",
                "--test_input",
                "tests/data/mock_test_input.json",
                "--eval_input",
                "tests/data/mock_eval_input.json",
                "--cromwell_job_id",
                "d9855002-6b71-429c-a4de-8e90222488cd",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--created_by",
                "glimmer@example.com",
                "--finished_before",
                "2020-10-00T00:00:00.000000",
                "--finished_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(name)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "Queen of Bright Moon run",
                "succeeded",
                '{"in_greeted": "Cool Person"}\n',
                '{"in_output_filename": "test_greeting.txt"}\n',
                "d9855002-6b71-429c-a4de-8e90222488cd",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "glimmer@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(name)",
                1,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                [
                    {
                        "created_at": "2020-09-16T18:48:06.371563",
                        "finished_at": "2020-09-16T18:58:06.371563",
                        "created_by": "glimmer@example.com",
                        "test_input": {"in_mother": "Angella"},
                        "eval_input": {"in_friend": "Bow"},
                        "status": "succeeded",
                        "results": {},
                        "cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                        "name": "Queen of Bright Moon run",
                        "test_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ]
            ),
        },
        {
            "args": ["test", "find_runs", "986325ba-06fe-4b1a-9e96-47d4f36bf819"],
            "params": [
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                20,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No runs found with the specified parameters",
                }
            ),
        },
        {
            "args": [
                "test",
                "find_runs",
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "--test_input",
                "nonexistent_file.json",
            ],
            "params": [],
            "return": "Failed to locate file with name nonexistent_file.json",
        },
    ]
)
def find_runs_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(runs).find(...).thenReturn(None)
    # Mock up request response
    if len(request.param["params"]) > 0:
        mockito.when(runs).find(
            "tests",
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
            request.param["params"][5],
            request.param["params"][6],
            request.param["params"][7],
            request.param["params"][8],
            request.param["params"][9],
            request.param["params"][10],
            request.param["params"][11],
            request.param["params"][12],
            request.param["params"][13],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_runs(find_runs_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_runs_data["args"])
    assert result.output == find_runs_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "subscribe",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "netossa@example.com",
            ],
            "params": ["cd987859-06fe-4b1a-9e96-47d4f36bf819", "netossa@example.com"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                    "entity_type": "test",
                    "entity_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "email": "netossa@example.com",
                    "created_at": "2020-09-23T19:41:46.839880",
                }
            ),
        },
        {
            "args": [
                "test",
                "subscribe",
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "spinnerella@example.com",
            ],
            "params": [
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "spinnerella@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No test found",
                    "status": 404,
                    "detail": "No test found with the specified ID",
                }
            ),
        },
        {
            "args": ["test", "subscribe", "89657859-06fe-4b1a-9e96-47d4f36bf819"],
            "params": ["89657859-06fe-4b1a-9e96-47d4f36bf819", "frosta@example.com"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                    "entity_type": "test",
                    "entity_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "email": "frosta@example.com",
                    "created_at": "2020-09-23T19:41:46.839880",
                }
            ),
        },
    ]
)
def subscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).subscribe(...).thenReturn(None)
    mockito.when(config).load_var_no_error("email").thenReturn("frosta@example.com")
    # Mock up request response
    mockito.when(tests).subscribe(
        request.param["params"][0], request.param["params"][1]
    ).thenReturn(request.param["return"])
    return request.param


def test_subscribe(subscribe_data):
    runner = CliRunner()
    result = runner.invoke(carrot, subscribe_data["args"])
    assert result.output == subscribe_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "test",
                "unsubscribe",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "netossa@example.com",
            ],
            "params": ["cd987859-06fe-4b1a-9e96-47d4f36bf819", "netossa@example.com"],
            "return": pprint.PrettyPrinter().pformat(
                {"message": "Successfully deleted 1 row(s)"}
            ),
        },
        {
            "args": [
                "test",
                "unsubscribe",
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "spinnerella@example.com",
            ],
            "params": [
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "spinnerella@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No subscription found",
                    "status": 404,
                    "detail": "No subscription found for the specified parameters",
                }
            ),
        },
        {
            "args": ["test", "unsubscribe", "89657859-06fe-4b1a-9e96-47d4f36bf819"],
            "params": ["89657859-06fe-4b1a-9e96-47d4f36bf819", "frosta@example.com"],
            "return": pprint.PrettyPrinter().pformat(
                {"message": "Successfully deleted 1 row(s)"}
            ),
        },
    ]
)
def unsubscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(tests).unsubscribe(...).thenReturn(None)
    mockito.when(config).load_var_no_error("email").thenReturn("frosta@example.com")
    # Mock up request response
    mockito.when(tests).unsubscribe(
        request.param["params"][0], request.param["params"][1]
    ).thenReturn(request.param["return"])
    return request.param


def test_unsubscribe(unsubscribe_data):
    runner = CliRunner()
    result = runner.invoke(carrot, unsubscribe_data["args"])
    assert result.output == unsubscribe_data["return"] + "\n"
