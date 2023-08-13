import boto3
import os 

class ParameterStoreFetcher:
    def __init__(self, region, logger):
        self.__logger = logger
        self.__region = region
        self.__client = boto3.client("ssm", 
                                    region_name=self.__region)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters.html
    def fetch_parameter_value(self, param_name, decryption=True):
        self.__logger.info(f"retrieving parameter {param_name}")
        return (
            self.__client.get_parameter(Name=param_name, WithDecryption=decryption)
            .get("Parameter")
            .get("Value")
        )
