import psycopg2
import logging

from src.aws.ssm import ParameterStoreFetcher

logging.basicConfig(format="[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s", level=logging.INFO, force=True)
logger = logging.getLogger()

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

		time_entry_table = """
			CREATE TABLE IF NOT EXISTS TimeEntry (
				id VARCHAR PRIMARY KEY,
				duration INT,
				project_id VARCHAR,
				description VARCHAR,
				end_timestamp TIMESTAMPTZ,
				start_timestamp TIMESTAMPTZ,
				duration_minutes FLOAT
			)
		"""
		self.cursor.execute(time_entry_table)

	def populate_database(self, tuples):
		sql = 'INSERT INTO timeentry VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET (duration, project_id, description, end_timestamp, start_timestamp, duration_minutes) = (EXCLUDED.duration, EXCLUDED.project_id, EXCLUDED.description, EXCLUDED.end_timestamp, EXCLUDED.start_timestamp, EXCLUDED.duration_minutes);'

		self.cursor.executemany(sql, tuples)

if __name__ == '__main__':
	conn = PostgresConnector(logger)
	# conn.cursor.execute('''
	# 	CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);
	# ''')
 