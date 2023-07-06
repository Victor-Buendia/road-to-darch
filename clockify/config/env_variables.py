import os
from os.path import join, dirname
from dotenv import load_dotenv

class Environment:
	def __init__(self):
		dotenv_path = join(dirname(__file__), '.env')
		load_dotenv(dotenv_path)
		self.BASE_URL = os.environ.get('BASE_URL')
		self.WORKSPACE_ID = os.environ.get('WORKSPACE_ID')
		self.API_KEY = os.environ.get('API_KEY')
		self.AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
		self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
		self.INTERVAL_DAYS = int(os.environ.get('INTERVAL_DAYS'))
		self.check_required_vars()

	class EnvironmentVariablesMissing(Exception):
			def __init__(self, missing):
				self.message = f"\nYour /config/.env file is missing the following variables: \n  " + '\n  '.join(missing)
				super().__init__(self.message)

	def check_required_vars(self):
		missing = []
		for variable, value in self.__dict__.items():
			if value == None:
				missing.append(variable)
		if len(missing) > 0:
			raise self.EnvironmentVariablesMissing(missing)