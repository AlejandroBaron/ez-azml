import inspect
from typing import Callable
from unittest import mock

from ez_azml.cloud_runs.pipelines import Pipeline


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


def test_pipeline_register_components(pipeline: Pipeline):
    """Tests that the components are properly decorated."""
    raw_functions = [c.function for c in pipeline.commands]
    registered_commands = pipeline._register_components(pipeline.commands)
    for raw_function, registered in zip(raw_functions, registered_commands):
        assert_function_wrapped(raw_function, registered.function)


def test_pipeline_setup_dec_kwargs(pipeline: Pipeline):
    """Tests that the pipeline decorator kwargs are properly postprocessed."""
    pipeline.dec_kwargs = pipeline._setup_dec_kwargs(pipeline.dec_kwargs)


def test_build_pipeline(pipeline: Pipeline):
    """Tests that the pipeline is properly decorated."""

    def f():
        pass

    with mock.patch.object(pipeline, "commands", return_value=f) as mocked:
        mocked.__name__ = "command_fn"

        raw_pipeline = pipeline.pipeline
        built_pipeline = pipeline._build_pipeline(raw_pipeline, pipeline.dec_kwargs)
        assert_function_wrapped(raw_pipeline, built_pipeline)
