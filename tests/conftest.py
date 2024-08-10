from pathlib import Path
from typing import Callable
from unittest import mock

import pytest
from azure.ai.ml import Input, MLClient, Output
from azure.ai.ml.entities import Environment
from ez_azml.cloud_runs import CommandRun, PipelineRun


@pytest.fixture()
def ml_client() -> MLClient:  # type: ignore
    """MLClient fixture."""
    mock_credential = mock.MagicMock()
    ml_client = MLClient(credential=mock_credential)
    with (
        mock.patch.object(ml_client.components, "create_or_update", return_value=True),
        mock.patch.object(ml_client.jobs, "create_or_update", return_value=True),
        mock.patch.object(
            ml_client.environments, "create_or_update", return_value=True
        ),
    ):
        yield ml_client


@pytest.fixture()
def conda_env_file() -> Path:
    """Path to a conda env file."""
    return Path(__file__).parent.parent / "configs/environments/conda.yaml"


@pytest.fixture()
def environment(conda_env_file: Path) -> Environment:
    """Environment fixture."""
    return Environment(
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
        name="test_environment",
        conda_file=str(conda_env_file),
    )


@pytest.fixture()
def command_code_path(tmp_path: Path) -> Path:
    """Points to tmp file."""
    path = tmp_path / "test_command.py"
    path.write_text("""
    print('this is a test command')
    """)
    return path


@pytest.fixture()
def command(ml_client: MLClient, command_code_path: Path, environment: Environment):
    """CommandRun fixture."""
    inputs = {"command_input": Input()}
    return CommandRun(
        ml_client=ml_client,
        code=command_code_path,
        commands="python command.py",
        environment=environment,
        inputs=inputs,
    )


@pytest.fixture()
def pipeline_fn() -> Callable:
    """Function used in azure.ai.ml pipelines."""

    def pipeline__fn(
        pipeline_input: Input,
        pipeline_output: Output,
    ):
        test_command(command_input=pipeline_input)  # type: ignore # noqa F821

    return pipeline__fn


@pytest.fixture()
def pipeline(ml_client: MLClient, pipeline_fn: Callable, command: CommandRun):
    """PipelineRun cloud run fixture."""
    return PipelineRun(
        ml_client=ml_client,
        experiment_name="fixture",
        commands=[command],
        pipeline=pipeline_fn,
    )
