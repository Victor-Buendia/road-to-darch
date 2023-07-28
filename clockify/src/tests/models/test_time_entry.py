from unittest.mock import Mock

import pytest

from models.time_entry import TimeEntry


@pytest.fixture
def event_obj():
    return {
        "totals": [
            {
                "_id": "",
                "totalTime": 574891,
                "totalBillableTime": 574891,
                "entriesCount": 106,
                "totalAmount": 0.0,
                "amounts": [{"type": "EARNED", "value": 0.0}],
            }
        ],
        "timeentries": [
            {
                "_id": "645d1e39b6abdc0c55a79d35",
                "description": "iFood",
                "userId": "5e95c064ea8094116e8e0a54",
                "timeInterval": {
                    "start": "2023-05-11T13:56:25-03:00",
                    "end": "2023-05-11T19:31:30-03:00",
                    "duration": 20105,
                },
                "billable": True,
                "projectId": "61e54e2ddc3256444ce00210",
                "taskId": None,
                "tagIds": None,
                "approvalRequestId": None,
                "isLocked": False,
                "amount": None,
                "rate": None,
                "userName": "Buendia",
                "userEmail": "victorbuendia03@gmail.com",
                "projectName": "iFood",
                "projectColor": "#F44336",
                "clientName": "",
                "clientId": "",
            },
            {
                "_id": "645ab58cb6abdc0c5573dbae",
                "description": "🔴🟡🔴 Clase de Español",
                "userId": "5e95c064ea8094116e8e0a54",
                "timeInterval": {
                    "start": "2023-05-09T18:05:15-03:00",
                    "end": "2023-05-09T19:11:48-03:00",
                    "duration": 3993,
                },
                "billable": True,
                "projectId": "5e9f4704ea8094116e994d87",
                "taskId": None,
                "tagIds": None,
                "approvalRequestId": None,
                "isLocked": False,
                "amount": None,
                "rate": None,
                "userName": "Buendia",
                "userEmail": "victorbuendia03@gmail.com",
                "projectName": "Capacitação",
                "projectColor": "#FFC107",
                "clientName": "",
                "clientId": "",
            },
        ],
    }


@pytest.fixture
def time_entry_list(event_obj):
    time_entry_list = TimeEntry.from_api_object_list(event_obj)
    return time_entry_list


@pytest.fixture
def unhealthy_event_obj():
    return {
        "totals": [
            {
                "_id": "",
                "totalTime": 574891,
                "totalBillableTime": 574891,
                "entriesCount": 106,
                "totalAmount": 0.0,
                "amounts": [{"type": "EARNED", "value": 0.0}],
            }
        ],
        "timeentries": [
            {
                "_id": "645d1e39b6abdc0c55a79d35",
                "userId": "5e95c064ea8094116e8e0a54",
                "timeInterval": {
                    "start": "2023-05-11T13:56:25-03:00",
                    "end": "2023-05-11T19:31:30-03:00",
                    "duration": 20105,
                },
                "billable": True,
                "projectId": "61e54e2ddc3256444ce00210",
                "taskId": None,
                "tagIds": None,
                "approvalRequestId": None,
                "isLocked": False,
                "amount": None,
                "rate": None,
                "userName": "Buendia",
                "userEmail": "victorbuendia03@gmail.com",
                "projectName": "iFood",
                "projectColor": "#F44336",
                "clientName": "",
                "clientId": "",
            }
        ],
    }


def test_should_initialize_successfully_when_healthy_entry_list_is_provided(
    time_entry_list,
):
    assert len(time_entry_list) == 2

    assert time_entry_list[0].id == "645d1e39b6abdc0c55a79d35"
    assert time_entry_list[0].duration == 20105
    assert time_entry_list[0].project_id == "61e54e2ddc3256444ce00210"
    assert time_entry_list[0].description == "iFood"
    assert time_entry_list[0].end_timestamp == "2023-05-11T19:31:30-03:00"
    assert time_entry_list[0].start_timestamp == "2023-05-11T13:56:25-03:00"
    assert time_entry_list[0].duration_minutes == 335.08

    assert time_entry_list[0].insert_tuple == (
        "645d1e39b6abdc0c55a79d35",
        20105,
        "61e54e2ddc3256444ce00210",
        "iFood",
        "2023-05-11T19:31:30-03:00",
        "2023-05-11T13:56:25-03:00",
        335.08,
    )

    assert time_entry_list[1].id == "645ab58cb6abdc0c5573dbae"
    assert time_entry_list[1].duration == 3993
    assert time_entry_list[1].project_id == "5e9f4704ea8094116e994d87"
    assert time_entry_list[1].description == "🔴🟡🔴 Clase de Español"
    assert time_entry_list[1].end_timestamp == "2023-05-09T19:11:48-03:00"
    assert time_entry_list[1].start_timestamp == "2023-05-09T18:05:15-03:00"
    assert time_entry_list[1].duration_minutes == 66.55

    assert time_entry_list[1].insert_tuple == (
        "645ab58cb6abdc0c5573dbae",
        3993,
        "5e9f4704ea8094116e994d87",
        "🔴🟡🔴 Clase de Español",
        "2023-05-09T19:11:48-03:00",
        "2023-05-09T18:05:15-03:00",
        66.55,
    )


def test_should_not_fail_when_unhealthy_entry_list_is_provided(unhealthy_event_obj):

    unhealthy_time_entry_list = TimeEntry.from_api_object_list(unhealthy_event_obj)

    assert len(unhealthy_time_entry_list) == 1
    assert unhealthy_time_entry_list[0].description is None
