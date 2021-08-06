import json

from click.testing import CliRunner

import mockito
import pytest
from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.config import manager as config
from carrot_cli.rest import runs, template_reports, template_results, templates


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
            "args": ["template", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This template will save Etheria",
                    "test_wdl": "example.com/she-ra_test.wdl",
                    "eval_wdl": "example.com/she-ra_eval.wdl",
                    "name": "Sword of Protection template",
                    "pipeline_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "title": "No template found",
                    "status": 404,
                    "detail": "No template found with the specified ID",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(templates).find_by_id(request.param["args"][2]).thenReturn(
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
                "template",
                "find",
                "--template_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--pipeline_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection template",
                "--pipeline_name",
                "Sword of Protection pipeline",
                "--description",
                "This template will save Etheria",
                "--test_wdl",
                "example.com/rebellion_test.wdl",
                "--eval_wdl",
                "example.com/rebellion_eval.wdl",
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
                "Sword of Protection template",
                "Sword of Protection pipeline",
                "This template will save Etheria",
                "example.com/rebellion_test.wdl",
                "example.com/rebellion_eval.wdl",
                "adora@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(name)",
                1,
                0,
            ],
            "return": json.dumps(
                [
                    {
                        "created_at": "2020-09-16T18:48:06.371563",
                        "created_by": "adora@example.com",
                        "description": "This template will save Etheria",
                        "test_wdl": "example.com/rebellion_test.wdl",
                        "eval_wdl": "example.com/rebellion_eval.wdl",
                        "name": "Sword of Protection template",
                        "pipeline_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ],
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "find",
                "--template_id",
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
            "return": json.dumps(
                {
                    "title": "No templates found",
                    "status": 404,
                    "detail": "No templates found with the specified parameters",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(templates).find(
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
                "template",
                "create",
                "--pipeline_id",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection template",
                "--description",
                "This template will save Etheria",
                "--test_wdl",
                "example.com/she-ra_test.wdl",
                "--eval_wdl",
                "example.com/she-ra_eval.wdl",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "Sword of Protection template",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "This template will save Etheria",
                "example.com/she-ra_test.wdl",
                "example.com/she-ra_eval.wdl",
                "adora@example.com",
            ],
            "return": json.dumps(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This template will save Etheria",
                    "test_wdl": "example.com/she-ra_test.wdl",
                    "eval_wdl": "example.com/she-ra_eval.wdl",
                    "name": "Sword of Protection template",
                    "pipeline_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "create",
                "--pipeline_id",
                "d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "Sword of Protection template",
                "--description",
                "This template will save Etheria",
                "--test_wdl",
                "example.com/she-ra_test.wdl",
                "--eval_wdl",
                "example.com/she-ra_eval.wdl",
            ],
            "params": [],
            "logging": "No email config variable set.  If a value is not specified for --created by, "
            "there must be a value set for email.",
        },
        {
            "args": ["template", "create"],
            "params": [],
            "return": "Usage: carrot_cli template create [OPTIONS]\n"
            "Try 'carrot_cli template create --help' for help.\n"
            "\n"
            "Error: Missing option '--pipeline_id'.",
        },
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).create(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(templates).create(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
            request.param["params"][5],
        ).thenReturn(request.param["return"])
    return request.param


def test_create(create_data, caplog):
    runner = CliRunner()
    result = runner.invoke(carrot, create_data["args"])
    if "logging" in create_data:
        assert create_data["logging"] in caplog.text
    else:
        assert result.output == create_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "update",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--description",
                "This new template replaced the broken one",
                "--name",
                "New Sword of Protection template",
                "--test_wdl",
                "example.com/she-ra_test.wdl",
                "--eval_wdl",
                "example.com/she-ra_eval.wdl",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "New Sword of Protection template",
                "This new template replaced the broken one",
                "example.com/she-ra_test.wdl",
                "example.com/she-ra_eval.wdl",
            ],
            "return": json.dumps(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This template replaced the broken one",
                    "test_wdl": "example.com/she-ra_test.wdl",
                    "eval_wdl": "example.com/she-ra_eval.wdl",
                    "name": "New Sword of Protection template",
                    "pipeline_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "update"],
            "params": [],
            "return": "Usage: carrot_cli template update [OPTIONS] ID\n"
            "Try 'carrot_cli template update --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).update(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(templates).update(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
        ).thenReturn(request.param["return"])
    return request.param


def test_update(update_data):
    runner = CliRunner()
    result = runner.invoke(carrot, update_data["args"])
    assert result.output == update_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": ["template", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row"}, indent=4, sort_keys=True
            ),
        },
        {
            "args": ["template", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "title": "No template found",
                    "status": 404,
                    "detail": "No template found with the specified ID",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def delete_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).delete(...).thenReturn(None)
    # Mock up request response
    mockito.when(templates).delete(request.param["args"][2]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_delete(delete_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_data["args"])
    assert result.output == delete_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
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
                "--test_cromwell_job_id",
                "d9855002-6b71-429c-a4de-8e90222488cd",
                "--eval_cromwell_job_id",
                "03958293-6b71-429c-a4de-8e90222488cd",
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
                {"in_greeted": "Cool Person"},
                {"in_output_filename": "test_greeting.txt"},
                "d9855002-6b71-429c-a4de-8e90222488cd",
                "03958293-6b71-429c-a4de-8e90222488cd",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "glimmer@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(name)",
                1,
                0,
            ],
            "return": json.dumps(
                [
                    {
                        "created_at": "2020-09-16T18:48:06.371563",
                        "finished_at": "2020-09-16T18:58:06.371563",
                        "created_by": "glimmer@example.com",
                        "test_input": {"in_mother": "Angella"},
                        "eval_input": {"in_friend": "Bow"},
                        "status": "succeeded",
                        "results": {},
                        "test_cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                        "eval_cromwell_job_id": "03958293-6b71-429c-a4de-8e90222488cd",
                        "name": "Queen of Bright Moon run",
                        "test_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ],
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "find_runs", "986325ba-06fe-4b1a-9e96-47d4f36bf819"],
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
                "",
                20,
                0,
            ],
            "return": json.dumps(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No runs found with the specified parameters",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "find_runs",
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "--test_input",
                "nonexistent_file.json",
            ],
            "params": [],
            "logging": "Encountered FileNotFound error when trying to read nonexistent_file.json",
        },
    ]
)
def find_runs_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(runs).find(...).thenReturn(None)
    # Mock up request response
    if len(request.param["params"]) > 0:
        mockito.when(runs).find(
            "templates",
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
            request.param["params"][14],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_runs(find_runs_data, caplog):
    runner = CliRunner()
    result = runner.invoke(carrot, find_runs_data["args"])
    if "logging" in find_runs_data:
        assert find_runs_data["logging"] in caplog.text
    else:
        assert result.output == find_runs_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "subscribe",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "netossa@example.com",
            ],
            "params": ["cd987859-06fe-4b1a-9e96-47d4f36bf819", "netossa@example.com"],
            "return": json.dumps(
                {
                    "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                    "entity_type": "template",
                    "entity_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "email": "netossa@example.com",
                    "created_at": "2020-09-23T19:41:46.839880",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "subscribe",
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "spinnerella@example.com",
            ],
            "params": [
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "spinnerella@example.com",
            ],
            "return": json.dumps(
                {
                    "title": "No template found",
                    "status": 404,
                    "detail": "No template found with the specified ID",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "subscribe", "89657859-06fe-4b1a-9e96-47d4f36bf819"],
            "params": ["89657859-06fe-4b1a-9e96-47d4f36bf819", "frosta@example.com"],
            "return": json.dumps(
                {
                    "subscription_id": "361b3b95-4a6e-40d9-bd98-f92b2959864e",
                    "entity_type": "template",
                    "entity_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "email": "frosta@example.com",
                    "created_at": "2020-09-23T19:41:46.839880",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def subscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).subscribe(...).thenReturn(None)
    mockito.when(config).load_var_no_error("email").thenReturn("frosta@example.com")
    # Mock up request response
    mockito.when(templates).subscribe(
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
                "template",
                "unsubscribe",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "netossa@example.com",
            ],
            "params": ["cd987859-06fe-4b1a-9e96-47d4f36bf819", "netossa@example.com"],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row(s)"}, indent=4, sort_keys=True
            ),
        },
        {
            "args": [
                "template",
                "unsubscribe",
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "--email",
                "spinnerella@example.com",
            ],
            "params": [
                "89657859-06fe-4b1a-9e96-47d4f36bf819",
                "spinnerella@example.com",
            ],
            "return": json.dumps(
                {
                    "title": "No subscription found",
                    "status": 404,
                    "detail": "No subscription found for the specified parameters",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "unsubscribe", "89657859-06fe-4b1a-9e96-47d4f36bf819"],
            "params": ["89657859-06fe-4b1a-9e96-47d4f36bf819", "frosta@example.com"],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row(s)"}, indent=4, sort_keys=True
            ),
        },
    ]
)
def unsubscribe_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(templates).unsubscribe(...).thenReturn(None)
    mockito.when(config).load_var_no_error("email").thenReturn("frosta@example.com")
    # Mock up request response
    mockito.when(templates).unsubscribe(
        request.param["params"][0], request.param["params"][1]
    ).thenReturn(request.param["return"])
    return request.param


def test_unsubscribe(unsubscribe_data):
    runner = CliRunner()
    result = runner.invoke(carrot, unsubscribe_data["args"])
    assert result.output == unsubscribe_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "map_to_result",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
                "adora@example.com",
            ],
            "return": json.dumps(
                {
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "result_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "result_key": "out_horde_tanks",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "map_to_result",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
            ],
            "params": [],
            "logging": "No email config variable set.  If a value is not specified for --created by, "
            "there must be a value set for email.",
        },
        {
            "args": ["template", "map_to_result"],
            "params": [],
            "return": "Usage: carrot_cli template map_to_result [OPTIONS] ID RESULT_ID RESULT_KEY\n"
            "Try 'carrot_cli template map_to_result --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def map_to_result_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_results).create_map(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_results).create_map(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
        ).thenReturn(request.param["return"])
    return request.param


def test_map_to_result(map_to_result_data, caplog):
    runner = CliRunner()
    result = runner.invoke(carrot, map_to_result_data["args"])
    if "logging" in map_to_result_data:
        assert map_to_result_data["logging"] in caplog.text
    else:
        assert result.output == map_to_result_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "find_result_map_by_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "result_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "result_key": "out_horde_tanks",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "find_result_map_by_id"],
            "params": [],
            "return": "Usage: carrot_cli template find_result_map_by_id [OPTIONS] ID RESULT_ID\n"
            "Try 'carrot_cli template find_result_map_by_id --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def find_result_map_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_results).find_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_results).find_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_result_map_by_id(find_result_map_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_result_map_by_id_data["args"])
    assert result.output == find_result_map_by_id_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "find_result_maps",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--result_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--result_key",
                "sword_of_protection_key",
                "--created_by",
                "adora@example.com",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(result_key)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "sword_of_protection_key",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "adora@example.com",
                "asc(result_key)",
                1,
                0,
            ],
            "return": json.dumps(
                [
                    {
                        "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                        "result_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "result_key": "sword_of_protection_key",
                        "created_at": "2020-09-24T19:07:59.311462",
                        "created_by": "adora@example.com",
                    }
                ],
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "find_result_maps",
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
                20,
                0,
            ],
            "return": json.dumps(
                {
                    "title": "No template_results found",
                    "status": 404,
                    "detail": "No template_results found with the specified parameters",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def find_result_maps_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_results).find_maps(...).thenReturn(None)
    # Mock up request response
    mockito.when(template_results).find_maps(
        request.param["params"][0],
        request.param["params"][1],
        request.param["params"][2],
        request.param["params"][3],
        request.param["params"][4],
        request.param["params"][5],
        request.param["params"][6],
        request.param["params"][7],
        request.param["params"][8],
    ).thenReturn(request.param["return"])
    return request.param


def test_find_result_maps(find_result_maps_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_result_maps_data["args"])
    assert result.output == find_result_maps_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "delete_result_map_by_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row"}, indent=4, sort_keys=True
            ),
        },
        {
            "args": ["template", "delete_result_map_by_id"],
            "params": [],
            "return": "Usage: carrot_cli template delete_result_map_by_id [OPTIONS] ID RESULT_ID\n"
            "Try 'carrot_cli template delete_result_map_by_id --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def delete_result_map_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_results).delete_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_results).delete_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_delete_result_map_by_id(delete_result_map_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_result_map_by_id_data["args"])
    assert result.output == delete_result_map_by_id_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "map_to_report",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "adora@example.com",
            ],
            "return": json.dumps(
                {
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "report_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "map_to_report",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [],
            "logging": "No email config variable set.  If a value is not specified for --created by, "
            "there must be a value set for email.",
        },
        {
            "args": ["template", "map_to_report"],
            "params": [],
            "return": "Usage: carrot_cli template map_to_report [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli template map_to_report --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def map_to_report_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_reports).create_map(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_reports).create_map(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
        ).thenReturn(request.param["return"])
    return request.param


def test_map_to_report(map_to_report_data, caplog):
    runner = CliRunner()
    result = runner.invoke(carrot, map_to_report_data["args"])
    if "logging" in map_to_report_data:
        assert map_to_report_data["logging"] in caplog.text
    else:
        assert result.output == map_to_report_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "find_report_map_by_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {
                    "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "report_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "input_map": {"section1": {"input1": "val1"}},
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                },
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": ["template", "find_report_map_by_id"],
            "params": [],
            "return": "Usage: carrot_cli template find_report_map_by_id [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli template find_report_map_by_id --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def find_report_map_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_reports).find_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_reports).find_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_report_map_by_id(find_report_map_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_report_map_by_id_data["args"])
    assert result.output == find_report_map_by_id_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "find_report_maps",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--report_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--created_by",
                "adora@example.com",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(input_map)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "adora@example.com",
                "asc(input_map)",
                1,
                0,
            ],
            "return": json.dumps(
                [
                    {
                        "template_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                        "report_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "created_at": "2020-09-24T19:07:59.311462",
                        "created_by": "adora@example.com",
                    }
                ],
                indent=4,
                sort_keys=True,
            ),
        },
        {
            "args": [
                "template",
                "find_report_maps",
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
            ],
            "params": [
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "",
                "",
                "",
                "",
                "",
                20,
                0,
            ],
            "return": json.dumps(
                {
                    "title": "No template_reports found",
                    "status": 404,
                    "detail": "No template_reports found with the specified parameters",
                },
                indent=4,
                sort_keys=True,
            ),
        },
    ]
)
def find_report_maps_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_reports).find_maps(...).thenReturn(None)
    # Mock up request response
    mockito.when(template_reports).find_maps(
        request.param["params"][0],
        request.param["params"][1],
        request.param["params"][2],
        request.param["params"][3],
        request.param["params"][4],
        request.param["params"][5],
        request.param["params"][6],
        request.param["params"][7],
    ).thenReturn(request.param["return"])
    return request.param


def test_find_report_maps(find_report_maps_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_report_maps_data["args"])
    assert result.output == find_report_maps_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "template",
                "delete_report_map_by_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row"}, indent=4, sort_keys=True
            ),
        },
        {
            "args": ["template", "delete_report_map_by_id"],
            "params": [],
            "return": "Usage: carrot_cli template delete_report_map_by_id [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli template delete_report_map_by_id --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def delete_report_map_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(template_reports).delete_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(template_reports).delete_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_delete_report_map_by_id(delete_report_map_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_report_map_by_id_data["args"])
    assert result.output == delete_report_map_by_id_data["return"] + "\n"
