from unittest.mock import Mock, call, patch
import unittest 
import pytest
import os

from configuration.clockify_configuration import ClockifyConfiguration


class TestClockifyConfiguration(unittest.TestCase):

    def setUp(self):
        os.environ["AWS_REGION"] = "us-east-1"
        os.environ["WORKSPACE_ID"] = "dummy_workspace"
        os.environ["INTERVAL_DAYS"] = "2"
        os.environ["API_KEY_SSM_PATH"] = "test-path-api-key"
        os.environ["DATABASE_USER_SSM_PATH"]="test-credentials.clockify.postgres-user"
        os.environ["DATABASE_PW_SSM_PATH"]="test-credentials.clockify.postgres-pw"
        os.environ["DATABASE_HOST_SSM_PATH"]="test-credentials.clockify.postgres-host"

    def tearDown(self):
        os.environ["AWS_REGION"] = ""
        os.environ["WORKSPACE_ID"] = ""
        os.environ["INTERVAL_DAYS"] = ""
        os.environ["API_KEY_SSM_PATH"] = ""
        os.environ["DATABASE_USER_SSM_PATH"]=""
        os.environ["DATABASE_PW_SSM_PATH"]=""
        os.environ["DATABASE_HOST_SSM_PATH"]=""



    def test_should_trigger_error_when_required_environment_variables_not_set(self):
        del os.environ["WORKSPACE_ID"]
        with patch("aws.ssm.ParameterStoreFetcher.fetch_parameter_value") as fetch,\
            pytest.raises(ClockifyConfiguration.EnvironmentVariablesMissing):
                logger = Mock()
                cfg = ClockifyConfiguration(logger)


    def test_build_from_environment_with_healthy_config(self):
        with patch("aws.ssm.ParameterStoreFetcher.fetch_parameter_value") as fetch:
            fetch.return_value = 'api_key_value'
            logger = Mock()
            cfg = ClockifyConfiguration(logger)

            calls = [call("test-path-api-key"),
                     call("test-credentials.clockify.postgres-host"),
                     call("test-credentials.clockify.postgres-user"),
                     call("test-credentials.clockify.postgres-pw")]
        
            assert cfg.WORKSPACE_ID == "dummy_workspace"
            assert cfg.INTERVAL_DAYS == 2
            assert cfg.API_KEY == "api_key_value"


            fetch.assert_has_calls(calls)

