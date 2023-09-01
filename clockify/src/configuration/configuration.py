import os
import logging
from os.path import join, dirname

class ClockifyConfiguration():
	def __init__(self, logger):
		self.__logger = logger

		self.required_variables = [
			"BASE_URL",
			"WORKSPACE_ID",
			"API_KEY",
			"INTERVAL_DAYS"
		]
		self.optional_variables = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
		self.check_required_vars()
		self.initialize_config_variables()

	def initialize_config_variables(self):
		self.BASE_URL = os.environ.get("BASE_URL")
		self.WORKSPACE_ID = os.environ.get("WORKSPACE_ID")
		self.API_KEY = os.environ.get("API_KEY")
		self.AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
		self.AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
		self.INTERVAL_DAYS = int(os.environ.get("INTERVAL_DAYS"))

	class EnvironmentVariablesMissing(Exception):
		def __init__(self, missing):
			self.message = (
				f"\nYour /config/.env file is missing the following variables: \n  "
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
			if variable not in os.environ:
				missing_variable_list.append(variable)
		return missing_variable_list
