import psycopg2

from aws.ssm import ParameterStoreFetcher

class PostgresConnector:
	def __init__(self, logger):
		self.__fetcher = ParameterStoreFetcher('us-east-1', logger)
		self.database_user = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-user')
		self.database_password = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-pw')
		self.host = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-host')

		self.establish_connection()

	def establish_connection(self):
		self.connection =  psycopg2.connect(
							database="db01",
							user=self.database_user,
							password=self.database_password,
							host=self.host,
							port='5432')

		self.connection.autocommit = True
		self.cursor = self.connection.cursor()
 