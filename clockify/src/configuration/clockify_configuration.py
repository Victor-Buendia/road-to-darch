import os
from os.path import join, dirname
from dotenv import load_dotenv

from aws.ssm import ParameterStoreFetcher

import logging

class ClockifyConfiguration():
	def __init__(self, logger):
		self.__logger = logger
		
		self.required_variables = [
			"AWS_REGION",
			"WORKSPACE_ID",
			"INTERVAL_DAYS",
			"API_KEY_SSM_PATH",
			"DATABASE_USER_SSM_PATH",
			"DATABASE_PW_SSM_PATH",
			"DATABASE_HOST_SSM_PATH"
		]
		self.optional_variables = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
		self.check_required_vars()
		self.initialize_simple_config_variables()
		self.__fetcher = ParameterStoreFetcher(self.AWS_REGION, logger)
		self.initialize_fetched_config_variables()

	def initialize_simple_config_variables(self):
		self.AWS_REGION = os.environ.get("AWS_REGION")
		self.WORKSPACE_ID = os.environ.get("WORKSPACE_ID")
		self.AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
		self.AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
		self.INTERVAL_DAYS = int(os.environ.get("INTERVAL_DAYS"))

	def initialize_fetched_config_variables(self):
		self.API_KEY = self.__fetcher.fetch_parameter_value(os.environ.get("API_KEY_SSM_PATH"))
		self.DATABASE_HOST = self.__fetcher.fetch_parameter_value(os.environ.get("DATABASE_HOST_SSM_PATH"))
		self.DATABASE_USER = self.__fetcher.fetch_parameter_value(os.environ.get("DATABASE_USER_SSM_PATH"))
		self.DATABASE_PW = self.__fetcher.fetch_parameter_value(os.environ.get("DATABASE_PW_SSM_PATH"))

	class EnvironmentVariablesMissing(Exception):
		def __init__(self, missing):
			self.message = (
				f"\nYour environment is missing the following variables: \n  "
				+ "\n  ".join(missing)
			)
			super().__init__(self.message)

	def check_required_vars(self):
		self.__logger.info("Checking environment variables")
		missing = self.check_variable_existence(self.required_variables)
		if len(missing) > 0:
			self.__logger.error(f"REQUIRED VARIABLES MISSING")
			raise self.EnvironmentVariablesMissing(missing)
		
		missing_optional = self.check_variable_existence(self.optional_variables)
		if len(missing_optional) > 0:
			missing_string = "\n ".join(missing_optional)
			self.__logger.warning(f"Optional variables missing: \n {missing_string}")

	
	def check_variable_existence(self, variable_list):
		missing_variable_list = []
		for variable in variable_list:
			if variable not in os.environ or os.environ.get(variable) == "":
				missing_variable_list.append(variable)
		return missing_variable_list
