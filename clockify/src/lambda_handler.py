import requests
import json
import pprint
import os
import logging
import datetime 
from models.time_entry import TimeEntry

from aws.ssm import ParameterStoreFetcher

logging.basicConfig(format="[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s", level=logging.INFO, force=True)
logger = logging.getLogger()

class Interactor:
	def __init__(self, workspace_id, logger):
		self.__fetcher = ParameterStoreFetcher('us-east-1', logger)
		self.__api_key = "ZDEwNzUwYjQtYzRmMi00M2NiLWE3MjMtZWU3YjEyY2ExOTlj" #self.__fetcher.fetch_parameter_value('prd-credentials.clockify.api-key')
		self.__workspace_id = workspace_id
		self.__api_date_format = "%Y-%m-%dT%H:%M:%S.%f%zZ"
		self.__logger = logger

	@property
	def base_endpoint(self):
		return (f'https://reports.api.clockify.me/v1/workspaces/{self.__workspace_id}')

	@property
	def detailed_reports_endpoint(self):
		return (os.path.join(self.base_endpoint.strip('/'), 'reports/detailed'))

	def generate_headers(self):
		headers = {'x-api-key': self.__api_key,
   				   'content-type': 'application/json'}
		return headers

	def generate_time_filters(self, end_date, interval_days):
		end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
		begin_date_object = end_date_object - datetime.timedelta(days=interval_days)
		
		date_filter = {'dateRangeStart': begin_date_object.strftime(self.__api_date_format),
					   'dateRangeEnd': end_date_object.strftime(self.__api_date_format),
					   'detailedFilter': {}}

		self.__logger.info(f"Date filter generated: from {begin_date_object} to {end_date_object}")

		return date_filter


	def fetch_detailed_reports(self, end_date=str(datetime.datetime.today()), interval_days=7):
		self.__logger.info(f"Retrieving detailed reports data.")
		headers = self.generate_headers()
		filters = self.generate_time_filters(end_date, interval_days)
		response = requests.post(self.detailed_reports_endpoint, headers=headers, json=filters)
		return response.text, response.status_code


workspace_id = '5e95c064ea8094116e8e0a56'
api_interactor = Interactor(workspace_id, logger)
print(api_interactor.base_endpoint)
print(api_interactor.detailed_reports_endpoint)
# date_filter = api_interactor.generate_time_filters(end_date='2023-05-12', interval_days=7)
# print(date_filter)
data, status = api_interactor.fetch_detailed_reports(end_date='2023-05-12', interval_days=7)

objs = TimeEntry.from_api_object_list(json.loads(data))

insert_list = [obj.insert_tuple for obj in objs]
print(insert_list)
# print(data)