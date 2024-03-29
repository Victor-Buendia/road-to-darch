import requests
import json
import os
import datetime
import math

from aws.ssm import ParameterStoreFetcher
from configuration.configuration import ClockifyConfiguration

class ApiInteractor:
    def __init__(self, logger):
        self.__fetcher = ParameterStoreFetcher("us-east-1", logger)
        self.__logger = logger
        self.__configuration = ClockifyConfiguration(self.__logger)
        self.__api_key = self.__fetcher.fetch_parameter_value(
            "prd-credentials.clockify.api-key"
        )
        self.__workspace_id = self.__configuration.WORKSPACE_ID
        self.__api_date_format = "%Y-%m-%dT%H:%M:%S.%f%zZ"
        self.__page_size = 50

    class UnexpectedStatusCode(Exception):
        def __init__(self, status_code):
            self.message = f"Status code {status_code} received from API."
            super().__init__(self.message)

    @property
    def base_endpoint(self):
        return f"https://reports.api.clockify.me/v1/workspaces/{self.__workspace_id}"

    @property
    def detailed_reports_endpoint(self):
        return os.path.join(self.base_endpoint.strip("/"), "reports/detailed")

    def generate_headers(self):
        headers = {"x-api-key": self.__api_key, "content-type": "application/json"}
        return headers

    def generate_time_filters(self, end_date, interval_days, current_page=1):
        end_date_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        begin_date_object = end_date_object - datetime.timedelta(days=interval_days)

        date_filter = {
            "dateRangeStart": begin_date_object.strftime(self.__api_date_format),
            "dateRangeEnd": end_date_object.strftime(self.__api_date_format),
            "detailedFilter": {"page": current_page, "pageSize": self.__page_size},
        }

        self.__logger.info(
            f"Date filter generated: from {begin_date_object} to {end_date_object} | Page: {current_page} | Page Size: {self.__page_size}"
        )

        return date_filter

    def retrieve_data(self, headers, filters):
        self.__logger.info(f"Retrieving detailed reports data.")
        response = requests.post(
            self.detailed_reports_endpoint, headers=headers, json=filters
        )
        data, status = json.loads(response.text), response.status_code
        self.validate_status(status)
        return data

    def validate_status(self, status_code):
        self.__logger.info(f"Validating API status code.")
        if status_code != 200:
            raise self.UnexpectedStatusCode(status_code)

    def calculate_total_pages(self, data):
        return math.ceil(data.get("totals")[0].get("entriesCount") / self.__page_size)
