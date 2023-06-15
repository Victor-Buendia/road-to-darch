import requests
import json
import pprint
import os
import logging
import datetime
import math

from utils.misc import deep_get
from models.time_entry import TimeEntry
from database.postgres_connector import PostgresConnector

from aws.ssm import ParameterStoreFetcher

logging.basicConfig(format="[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s", level=logging.INFO, force=True)
logger = logging.getLogger()

class Interactor:
	def __init__(self, workspace_id, logger):
		self.__fetcher = ParameterStoreFetcher('us-east-1', logger)
		self.__api_key = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.api-key')
		self.__workspace_id = workspace_id
		self.__api_date_format = "%Y-%m-%dT%H:%M:%S.%f%zZ"
		self.__logger = logger
		self.__page_size = 50
		self.__conn = PostgresConnector(logger)

	class UnexpectedStatusCode(Exception):
		def __init__(self, status_code):
			self.message = f"Status code {status_code} received from API."
			super().__init__(self.message)

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

	def generate_time_filters(self, end_date, interval_days, current_page=1):
		end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
		begin_date_object = end_date_object - datetime.timedelta(days=interval_days)
		
		date_filter = {'dateRangeStart': begin_date_object.strftime(self.__api_date_format),
					   'dateRangeEnd': end_date_object.strftime(self.__api_date_format),
					   'detailedFilter': {'page': current_page, 'pageSize': self.__page_size}}

		self.__logger.info(f"Date filter generated: from {begin_date_object} to {end_date_object} | Page: {current_page} | Page Size: {self.__page_size}")

		return date_filter

	def retrieve_data(self, headers, filters):
		self.__logger.info(f"Retrieving detailed reports data.")
		response = requests.post(self.detailed_reports_endpoint, headers=headers, json=filters)
		data, status = json.loads(response.text), response.status_code
		self.validate_status(status)
		return data

	def validate_status(self, status_code):
		self.__logger.info(f"Validating API status code.")
		if status_code != 200:
			raise self.UnexpectedStatusCode(status_code)

	def generate_time_entry_insert_list(self, data):
		self.__logger.info(f"Generating Time Entry insert list.")
		objs = TimeEntry.from_api_object_list(data)
		insert_list = [obj.insert_tuple for obj in objs]
		return insert_list

	def postgres_insert(self, insert_list):
		self.__logger.info(f"Populating data.")
		self.__conn.populate_database(tuples=insert_list)
		self.__logger.info(f"Done populating DB.\n")

	def fetch_and_insert_detailed_reports(self, end_date=str(datetime.datetime.today()), interval_days=7):
		self.__logger.info(f"Starting fetch process.")
		headers = self.generate_headers()

		current_page = total_pages = 1
		while current_page <= total_pages:
			filters = self.generate_time_filters(end_date, interval_days, current_page)
			data = self.retrieve_data(headers=headers, filters=filters)

			insert_list = self.generate_time_entry_insert_list(data)
			self.postgres_insert(insert_list=insert_list)

			total_pages = math.ceil(data.get('totals')[0].get('entriesCount')/self.__page_size)
			current_page += 1
		self.__logger.info(f"Fetching and populating ended for {total_pages} pages with {data.get('totals')[0].get('entriesCount')} entries.")

workspace_id = '5e95c064ea8094116e8e0a56'
api_interactor = Interactor(workspace_id, logger)
api_interactor.fetch_and_insert_detailed_reports(end_date='2023-05-12', interval_days=365)