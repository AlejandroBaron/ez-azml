import inspect
from typing import Callable
from unittest import mock

from ez_azml.cloud_runs.pipelines import PipelineRun


def assert_function_wrapped(function: Callable, wrapped_function: Callable) -> None:
    """Asserts that a function is properly wrapped.

    Args:
        wrapped_function: The function that is potentially wrapped.
        function: The original function to compare against after unwrapping.

    Raises:
        AssertionError: If the function is already wrapped or if unwrapping the wrapped
                        function does not yield the original function.
    """
    assert not hasattr(function, "__wrapped__"), "The function should not be wrapped."
    assert (
        inspect.unwrap(wrapped_function) is function
    ), "Unwrapping the wrapped function did not yield the original function."


def test_pipeline_register(pipeline: PipelineRun):
    """Tests that the components are properly decorated."""

    def mock_create(*args, **kwargs):
        pass

    with mock.patch.object(
        pipeline, "ml_client.jobs.create_or_update", return_value=mock_create
    ) as mocked:
        pipeline.register()
        print(mocked)
