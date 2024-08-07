from typing import Callable

import mldesigner as mld
import pytest
from azure.ai.ml import Input, Output
from ez_azml.cloud_runs.pipelines import Pipeline, PipelineCommand


@pytest.fixture()
def command_fn() -> Callable:
    """Function used in mldesigner command component."""

    def _command_fn(
        command_input: mld.Input(type="uri_folder"),  # type: ignore
        command_output: mld.Output(type="uri_folder"),  # type: ignore
    ):
        print("this is a test_fn")

    return _command_fn


@pytest.fixture()
def pipeline_fn(command_fn) -> Callable:
    """Function used in azure.ai.ml pipelines."""

    def _pipeline_fn(
        pipeline_input: Input,
        pipeline_output: Output,
    ):
        command_fn(pipeline_input)

    return _pipeline_fn


@pytest.fixture()
def pipeline_command(command_fn: Callable):
    """PipelineCommand fixture."""
    return PipelineCommand(function=command_fn)


@pytest.fixture()
def pipeline(pipeline_fn: Callable, pipeline_command: PipelineCommand):
    """Pipeline cloud run fixture."""
    return Pipeline(
        experiment_name="fixture",
        commands=[pipeline_command],
        pipeline=pipeline_fn,
    )
