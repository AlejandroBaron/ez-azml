from pathlib import Path
from typing import Callable

import pytest
from azure.ai.ml import Input, Output
from ez_azml.cloud_runs import CommandRun, PipelineRun


@pytest.fixture()
def command_code_path(tmp_path: Path) -> Path:
    """Points to tmp file."""
    path = tmp_path / "test_command.py"
    path.write_text("""
    print('this is a test command')
    """)
    return path


@pytest.fixture()
def command(command_code_path: Path):
    """CommandRun fixture."""
    return CommandRun(code=command_code_path, commands="python command.py")


@pytest.fixture()
def pipeline_fn(command_fn) -> Callable:
    """Function used in azure.ai.ml pipelines."""

    def pipeline__fn(
        pipeline_input: Input,
        pipeline_output: Output,
    ):
        test_command(pipeline_input)  # noqa F821

    return pipeline__fn


@pytest.fixture()
def pipeline(pipeline_fn: Callable, command: CommandRun):
    """PipelineRun cloud run fixture."""
    return PipelineRun(
        experiment_name="fixture",
        commands=[command],
        pipeline=pipeline_fn,
    )
