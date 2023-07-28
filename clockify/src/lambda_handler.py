import datetime
import math
import logging

from models.time_entry import TimeEntry
from models.clockify_api_interactor import ApiInteractor
from database.postgres_connector import PostgresConnector
from aws.ssm import ParameterStoreFetcher


def lambda_handler(event, context):
    logging.basicConfig(
        format="[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s",
        level=logging.INFO,
        force=True,
    )
    logger = logging.getLogger()

    workspace_id = "5e95c064ea8094116e8e0a56"
    end_date = "2023-05-12"
    interval_days = 30
    api_key_ssm_path = "prd-credentials.clockify.api-key"

    fetcher = ParameterStoreFetcher("us-east-1", logger)
    api_key = fetcher.fetch_parameter_value(api_key_ssm_path)
    api_interactor = ApiInteractor(workspace_id, api_key, logger)
    headers = api_interactor.generate_headers()

    conn = PostgresConnector(logger)

    logger.info(f"Starting fetch process.")

    current_page = total_pages = 1
    while current_page <= total_pages:
        filters = api_interactor.generate_time_filters(
            end_date, interval_days, current_page
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
