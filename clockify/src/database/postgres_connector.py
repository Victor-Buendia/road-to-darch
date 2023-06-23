import psycopg2

from aws.ssm import ParameterStoreFetcher

class PostgresConnector:
	def __init__(self, logger):
		self.__fetcher = ParameterStoreFetcher('us-east-1', logger)
		self.database_user = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-user')
		self.database_password = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-pw')
		self.host = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.postgres-host')
		self.__logger = logger 
		self.establish_connection()

	def establish_connection(self):
		self.__logger.info(f"Establishing connection to database.")
		self.connection =  psycopg2.connect(
							database="db01",
							user=self.database_user,
							password=self.database_password,
							host=self.host,
							port='5432')

		self.connection.autocommit = True
		self.cursor = self.connection.cursor()

		time_entry_table = """
			CREATE TABLE IF NOT EXISTS timeentry (
				id VARCHAR PRIMARY KEY,
				duration INT,
				project_id VARCHAR,
				description VARCHAR,
				end_timestamp TIMESTAMPTZ,
				start_timestamp TIMESTAMPTZ,
				duration_minutes FLOAT,
				updated_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
			)
		"""
		self.__logger.info(f"Running create table if not exists.")
		self.cursor.execute(time_entry_table)

	def populate_database(self, tuples):
		self.__logger.info(f"Inserting data with length {len(tuples)}.")
		sql = 'INSERT INTO timeentry VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET (duration, project_id, description, end_timestamp, start_timestamp, duration_minutes, updated_at) = (EXCLUDED.duration, EXCLUDED.project_id, EXCLUDED.description, EXCLUDED.end_timestamp, EXCLUDED.start_timestamp, EXCLUDED.duration_minutes, current_timestamp);'

		self.cursor.executemany(sql, tuples)
		self.__logger.info(f"Data successfully inserted.")

 