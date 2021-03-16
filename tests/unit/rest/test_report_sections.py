import pprint

import mockito
import pytest

from carrot_cli.rest import request_handler, report_sections


@pytest.fixture(
    params=[
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "position": "1",
            "created_by": "rogelio@example.com",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "name": "Horde Tanks Section",
                    "position":1,
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                }
            ),
        },
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "position": "1",
            "created_by": "rogelio@example.com",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "Server error",
                    "status": 500,
                    "detail": "Error while attempting to insert new report section mapping",
                }
            ),
        },
    ]
)
def create_map_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).create_map(...).thenReturn(None)
    # Mock up request response
    params = [
        ("name", request.param["name"]),
        ("position", request.param["position"]),
        ("created_by", request.param["created_by"]),
    ]
    mockito.when(request_handler).create_map(
        "reports",
        request.param["report_id"],
        "sections",
        request.param["section_id"],
        params,
    ).thenReturn(request.param["return"])
    return request.param


def test_create_map(create_map_data):
    section = report_sections.create_map(
        create_map_data["report_id"],
        create_map_data["section_id"],
        create_map_data["name"],
        create_map_data["position"],
        create_map_data["created_by"],
    )
    assert section == create_map_data["return"]


@pytest.fixture(
    params=[
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "params": [
                ("section_id", "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("name", "Horde Tanks Section"),
                ("position", ""),
                ("created_before", ""),
                ("created_after", ""),
                ("created_by", "rogelio@example.com"),
                ("sort", ""),
                ("limit", ""),
                ("offset", ""),
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "name": "Horde Tanks Section",
                    "position":"1",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                }
            ),
        },
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "params": [
                ("section_id", "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("name", "Horde Tanks Sections"),
                ("position", ""),
                ("created_before", ""),
                ("created_after", ""),
                ("created_by", ""),
                ("sort", ""),
                ("limit", ""),
                ("offset", ""),
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No report_section mapping found",
                    "status": 404,
                    "detail": "No report_section mapping found with the specified parameters",
                }
            ),
        },
    ]
)
def find_maps_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find_maps(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find_maps(
        "reports", request.param["report_id"], "sections", request.param["params"]
    ).thenReturn(request.param["return"])
    return request.param


def test_find_maps(find_maps_data):
    section = report_sections.find_maps(
        find_maps_data["report_id"],
        find_maps_data["params"][0][1],
        find_maps_data["params"][1][1],
        find_maps_data["params"][2][1],
        find_maps_data["params"][3][1],
        find_maps_data["params"][4][1],
        find_maps_data["params"][5][1],
        find_maps_data["params"][6][1],
        find_maps_data["params"][7][1],
        find_maps_data["params"][8][1]
    )
    assert section == find_maps_data["return"]


@pytest.fixture(
    params=[
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "name": "Horde Tanks Section",
                    "position": "1",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                }
            ),
        },
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No report_section mapping found",
                    "status": 404,
                    "detail": "No report_section mapping found with the specified IDs and name",
                }
            ),
        },
    ]
)
def find_map_by_ids_and_name_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).find_map_by_ids_and_name(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find_map_by_ids_and_name(
        "reports", request.param["report_id"], "sections", request.param["section_id"],
        request.param["name"]
    ).thenReturn(request.param["return"])
    return request.param


def test_find_maps_by_ids_and_name(find_map_by_ids_and_name_data):
    section = report_sections.find_map_by_ids_and_name(
        find_map_by_ids_and_name_data["report_id"], find_map_by_ids_and_name_data["section_id"],
        find_map_by_ids_and_name_data["name"]
    )
    assert section == find_map_by_ids_and_name_data["return"]

@pytest.fixture(
    params=[
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
            "name": "Horde Tanks Section",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No report_section mapping found",
                    "status": 404,
                    "detail": "No report_section mapping found with the specified IDs and name",
                }
            ),
        },
    ]
)
def delete_map_by_ids_and_name_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).delete_map_by_ids_and_name(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).delete_map_by_ids_and_name(
        "reports", request.param["report_id"], "sections", request.param["section_id"],
        request.param["name"]
    ).thenReturn(request.param["return"])
    return request.param


def test_delete_maps_by_ids_and_name(delete_map_by_ids_and_name_data):
    section = report_sections.delete_map_by_ids_and_name(
        delete_map_by_ids_and_name_data["report_id"], delete_map_by_ids_and_name_data["section_id"],
        delete_map_by_ids_and_name_data["name"]
    )
    assert section == delete_map_by_ids_and_name_data["return"]
