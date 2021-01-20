import pprint

import mockito
import pytest
from click.testing import CliRunner

from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.rest import runs


@pytest.fixture(autouse=True)
def unstub():
    yield
    mockito.unstub()


@pytest.fixture(
    params=[
        {
            "args": ["run", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
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
                }
            ),
        },
        {
            "args": ["run", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No run found with the specified ID",
                }
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
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "args": ["run", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No run found",
                    "status": 404,
                    "detail": "No run found with the specified ID",
                }
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
