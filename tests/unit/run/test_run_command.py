import json

from click.testing import CliRunner

import mockito
import pytest
from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.config import manager as config
from carrot_cli.rest import run_reports, runs


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
            "args": ["run", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "finished_at": None,
                    "created_by": "adora@example.com",
                    "test_input": {"in_prev_owner": "Mara"},
                    "eval_input": {"in_creators": "Old Ones"},
                    "status": "testsubmitted",
                    "results": {},
                    "test_cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                    "eval_cromwell_job_id": "39482203-6b71-429c-a4de-8e90222488cd",
                    "name": "Sword of Protection run",
                    "test_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                },
                indent=4, sort_keys=True
            ),
        },
        {
            "args": ["run", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No run found with the specified ID",
                },
                indent=4, sort_keys=True
            ),
        },
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(runs).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(runs).find_by_id(request.param["args"][2]).thenReturn(
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
            "args": ["run", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row"},
                indent=4, sort_keys=True
            ),
        },
        {
            "args": ["run", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": json.dumps(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No run found with the specified ID",
                },
                indent=4, sort_keys=True
            ),
        },
    ]
)
def delete_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(runs).delete(...).thenReturn(None)
    # Mock up request response
    mockito.when(runs).delete(request.param["args"][2]).thenReturn(
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
                "run",
                "create_report",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--created_by",
                "adora@example.com",
                "--delete_failed",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "adora@example.com",
                True,
            ],
            "return": json.dumps(
                {
                    "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "report_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "status": "created",
                    "cromwell_job_id": None,
                    "results": {},
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "adora@example.com",
                    "finished_at": None,
                },
                indent=4, sort_keys=True
            ),
        },
        {
            "args": [
                "run",
                "create_report",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [],
            "logging": "No email config variable set.  If a value is not specified for --created by, "
            "there must be a value set for email.",
        },
        {
            "args": ["run", "create_report"],
            "params": [],
            "return": "Usage: carrot_cli run create_report [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli run create_report --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def create_report_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(run_reports).create_map(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(run_reports).create_map(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
        ).thenReturn(request.param["return"])
    return request.param


def test_create_report(create_report_data, caplog):
    runner = CliRunner()
    result = runner.invoke(carrot, create_report_data["args"])
    if "logging" in create_report_data:
        assert create_report_data["logging"] in caplog.text
    else:
        assert result.output == create_report_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "run",
                "find_report_by_ids",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {
                    "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "report_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "status": "succeeded",
                    "cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                    "results": {"result1": "val1"},
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                    "finished_at": "2020-09-24T21:07:59.311462",
                },
                indent=4, sort_keys=True
            ),
        },
        {
            "args": ["run", "find_report_by_ids"],
            "params": [],
            "return": "Usage: carrot_cli run find_report_by_ids [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli run find_report_by_ids --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def find_report_by_ids_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(run_reports).find_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(run_reports).find_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_report_by_ids(find_report_by_ids_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_report_by_ids_data["args"])
    assert result.output == find_report_by_ids_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "run",
                "find_reports",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--report_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--status",
                "succeeded",
                "--cromwell_job_id",
                "d9855002-6b71-429c-a4de-8e90222488cd",
                "--results",
                "tests/data/mock_report_results.json",
                "--created_by",
                "adora@example.com",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--finished_before",
                "2020-10-00T00:00:00.000000",
                "--finished_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(status)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "succeeded",
                "d9855002-6b71-429c-a4de-8e90222488cd",
                {"result1": "val1"},
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "adora@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(status)",
                1,
                0,
            ],
            "return": json.dumps(
                [
                    {
                        "run_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                        "report_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "status": "succeeded",
                        "cromwell_job_id": "d9855002-6b71-429c-a4de-8e90222488cd",
                        "results": {"result1": "val1"},
                        "created_at": "2020-09-24T19:07:59.311462",
                        "created_by": "adora@example.com",
                        "finished_at": "2020-09-24T21:07:59.311462",
                    }
                ],
                indent=4, sort_keys=True
            ),
        },
        {
            "args": [
                "run",
                "find_reports",
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
                    "title": "No run_reports found",
                    "status": 404,
                    "detail": "No run_reports found with the specified parameters",
                },
                indent=4, sort_keys=True
            ),
        },
    ]
)
def find_reports_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(run_reports).find_maps(...).thenReturn(None)
    # Mock up request response
    mockito.when(run_reports).find_maps(
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


def test_find_reports(find_reports_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_reports_data["args"])
    assert result.output == find_reports_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "run",
                "delete_report_by_ids",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            ],
            "return": json.dumps(
                {"message": "Successfully deleted 1 row"},
                indent=4, sort_keys=True
            ),
        },
        {
            "args": ["run", "delete_report_by_ids"],
            "params": [],
            "return": "Usage: carrot_cli run delete_report_by_ids [OPTIONS] ID REPORT_ID\n"
            "Try 'carrot_cli run delete_report_by_ids --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def delete_report_by_ids_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(run_reports).delete_map_by_ids(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(run_reports).delete_map_by_ids(
            request.param["params"][0],
            request.param["params"][1],
        ).thenReturn(request.param["return"])
    return request.param


def test_delete_report_by_ids(delete_report_by_ids_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_report_by_ids_data["args"])
    assert result.output == delete_report_by_ids_data["return"] + "\n"
