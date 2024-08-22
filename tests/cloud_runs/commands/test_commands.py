import os
from pathlib import Path
from unittest import mock

import yaml
from azure.ai.ml.entities import CommandComponent
from ez_azml.cloud_runs import CommandRun


def test_get_component_yaml(command: CommandRun, command_code_path: Path):
    """Tests that the yaml is properly generated."""
    yaml_io = command._get_component_yaml_stream(**command.register_kwargs)
    expected_yaml = {
        "code": str(command_code_path),
        "command": "python command.py",
        "environment": "azureml:test_environment:1",
        "inputs": {"command_input": {"type": "uri_folder"}},
        "name": "test_command",
        "outputs": {},
    }
    assert expected_yaml == yaml.safe_load(yaml_io)


def test_e2e_register(command: CommandRun):
    """Tests e2e mock register."""
    component = command.register()
    assert isinstance(component, CommandComponent)


def test_command_kwargs_env_parsing(command: CommandRun):
    """Tests that parsing env variables works when processing command kwargs."""

    REMOTE_KEY = "REMOTE_ENV"
    LOCAL_KEY = "LOCAL_ENV"
    mock_env_value = "mock_env_value"
    command_kwargs = {"environment_variables": {REMOTE_KEY: LOCAL_KEY}}
    with mock.patch.dict(os.environ, {LOCAL_KEY: mock_env_value}):
        parsed_command_kwargs = command._process_command_kwargs(command_kwargs)
    assert parsed_command_kwargs["environment_variables"][REMOTE_KEY] == mock_env_value
