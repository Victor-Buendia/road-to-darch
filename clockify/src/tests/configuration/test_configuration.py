from unittest.mock import Mock, call, patch

import pytest
import os

from configuration.clockify_configuration import ClockifyConfiguration


def setup_module():
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["WORKSPACE_ID"] = "ssm_path_env"
    os.environ["INTERVAL_DAYS"] = "2"
    os.environ["API_KEY_SSM_PATH"] = "test-path-api-key"


def teardown_module():
    os.environ["AWS_REGION"] = ""
    os.environ["WORKSPACE_ID"] = ""
    os.environ["INTERVAL_DAYS"] = ""
    os.environ["API_KEY_SSM_PATH"] = ""


def test_should_trigger_error_when_required_environment_variables_not_set():
    setup_module()
    del os.environ["WORKSPACE_ID"]
    with patch("aws.ssm.ParameterStoreFetcher.fetch_parameter_value") as fetch,\
        pytest.raises(ClockifyConfiguration.EnvironmentVariablesMissing):
            logger = Mock()
            cfg = ClockifyConfiguration(logger)


def test_build_from_environment_with_healthy_config():
    with patch("aws.ssm.ParameterStoreFetcher.fetch_parameter_value") as fetch:
        fetch.return_value = 'api_key_value'
        setup_module()
        logger = Mock()
        cfg = ClockifyConfiguration(logger)
    
        assert cfg.WORKSPACE_ID == "ssm_path_env"
        assert cfg.INTERVAL_DAYS == 2
        assert cfg.API_KEY == "api_key_value"

