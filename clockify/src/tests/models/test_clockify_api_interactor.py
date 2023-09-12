from unittest.mock import Mock, patch

import pytest

from models.clockify_api_interactor import ApiInteractor


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
def api_interactor():
    logger = Mock()
    api_key = 'test_key'
    workspace_id = 'myworkspace'
    api_interactor = ApiInteractor(logger, workspace_id, api_key)
    return api_interactor


def test_should_generate_correct_base_endpoint_when_valid_values_are_passed(
    api_interactor,
):
    assert api_interactor.base_endpoint == 'https://reports.api.clockify.me/v1/workspaces/myworkspace'


def test_should_build_correct_reports_endpoint_when_valid_values_are_passed(api_interactor):
    assert api_interactor.detailed_reports_endpoint == 'https://reports.api.clockify.me/v1/workspaces/myworkspace/reports/detailed'

def test_should_build_correct_headers_when_valid_values_are_passed(api_interactor):
    assert api_interactor.generate_headers() == {"x-api-key":'test_key', 'content-type': 'application/json'}

def test_should_generate_correct_time_filters_when_no_current_page_is_passed(api_interactor):
    
    date_filter = api_interactor.generate_time_filters('2023-01-01', 6)
    assert date_filter == {'dateRangeEnd': '2023-01-01T00:00:00.000000Z', 'dateRangeStart': '2022-12-26T00:00:00.000000Z', 'detailedFilter': {'page': 1, 'pageSize': 50}}


def test_should_generate_correct_time_filters_when_current_page_is_passed(api_interactor):
    
    date_filter = api_interactor.generate_time_filters('2023-01-01', 6, 5)
    assert date_filter == {'dateRangeEnd': '2023-01-01T00:00:00.000000Z', 'dateRangeStart': '2022-12-26T00:00:00.000000Z', 'detailedFilter': {'page': 5, 'pageSize': 50}}


def test_should_retrieve_data_correctly_when_status_200(api_interactor):
    with patch("models.clockify_api_interactor.requests.post") as req:
        res = Mock()
        res.ok = True
        res.status_code = 200
        res.text = '{"super_valid_data":"asdfg"}'
        req.return_value = res

        
        headers = api_interactor.generate_headers()
        filters = api_interactor.generate_time_filters('2022-01-01', 10, 5)

        data = api_interactor.retrieve_data(headers, filters)
        assert data == {'super_valid_data': 'asdfg'}

def test_should_trigger_error_when_status_not_200(api_interactor):
    with patch("models.clockify_api_interactor.requests.post") as req:
        res = Mock()
        res.ok = True
        res.status_code = 201
        res.text = '{"super_valid_data":"asdfg"}'
        req.return_value = res

        
        headers = api_interactor.generate_headers()
        filters = api_interactor.generate_time_filters('2022-01-01', 10, 5)
        with pytest.raises(ApiInteractor.UnexpectedStatusCode):
            api_interactor.retrieve_data(headers, filters)

def test_should_calculate_total_pages_correctly(api_interactor):
    data = {'totals':[{'entriesCount':354}]}
    pages = api_interactor.calculate_total_pages(data)
    assert pages == 8