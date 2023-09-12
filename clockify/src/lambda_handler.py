import datetime
import math
import logging
import os

from models.time_entry import TimeEntry
from models.clockify_api_interactor import ApiInteractor
from database.postgres_connector import PostgresConnector
from configuration.clockify_configuration import ClockifyConfiguration

def lambda_handler(event, context):
    logging.basicConfig(
        format="[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s",
        level=logging.INFO,
        force=True,
    )
    logger = logging.getLogger()
    configuration = ClockifyConfiguration(logger)

    end_date = "2023-05-12"

    api_interactor = ApiInteractor(logger, configuration.WORKSPACE_ID, configuration.API_KEY)
    headers = api_interactor.generate_headers()

    conn = PostgresConnector(logger, configuration.DATABASE_HOST, configuration.DATABASE_USER, configuration.DATABASE_PW)

    logger.info(f"Starting fetch process.")

    current_page = total_pages = 1
    while current_page <= total_pages:
        filters = api_interactor.generate_time_filters(
            end_date, configuration.INTERVAL_DAYS, current_page
        )
        data = api_interactor.retrieve_data(headers=headers, filters=filters)

        time_entry_insert_list = generate_time_entry_insert_list(data, logger)

        conn.populate_database(tuples=time_entry_insert_list)
        total_pages = api_interactor.calculate_total_pages(data)
        current_page += 1

    logger.info(
        f"Fetching and populating ended for {total_pages} pages with {data.get('totals')[0].get('entriesCount')} entries."
    )


def generate_time_entry_insert_list(data, logger):
    logger.info(f"Generating Time Entry insert list.")
    objs = TimeEntry.from_api_object_list(data)
    insert_list = [obj.insert_tuple for obj in objs]
    return insert_list


if __name__ == "__main__":
    lambda_handler("", "")
