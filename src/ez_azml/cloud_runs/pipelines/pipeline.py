import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import mldesigner as mld
from azure.ai.ml.dsl import pipeline as pipeline_dec
from azure.ai.ml.entities import Environment
from typing_extensions import override

from ez_azml.cloud_runs.cloud_run import CloudRun, RunOutput


@dataclass
class Command:
    """Class representing a mldesigner Azureml step (mldesigner.command_component).

    Args:
        function: function to be decorated
        environment: enviroment to run the comand at
        component_kwargs: kwargs to pass to the `mldesigner.command_component` decorator
    """

    function: Callable
    environment: Optional[Environment] = None
    component_kwargs: Optional[dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        self.component_kwargs["environment"] = self.environment


class Pipeline(CloudRun):
    """Cloud run that uses mldesigner pipelines.

    Args:
        experiment_name: experiment this pipeline is associated with
        commands: commands to use within the pipeline
        pipeline: function representing the pipeline
        dec_kwargs: kwargs for azure.ai.ml.dsl.pipeline decorator
    """

    def __init__(
        self,
        experiment_name: str,
        commands: list[Command],
        pipeline: Callable,
        dec_kwargs: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.experiment_name = experiment_name
        self.commands = commands
        self.dec_kwargs = dec_kwargs or {}
        self.pipeline = pipeline

    def _register_components(self, commands: list[Command]) -> list[Callable]:
        decorated = []
        kwargs_pattern = r"(\w+)\s*=\s*(['\"]?)(\w+)\2"
        for command in commands:
            fn = command.function
            for parameter in fn.__annotations__:
                hint = fn.__annotations__[parameter]
                if isinstance(hint, str):
                    potential_kwargs = {
                        key: value for key, _, value in re.findall(kwargs_pattern, hint)
                    }
                    if "Input(" in hint:
                        hint = mld.Input(**potential_kwargs)
                    elif "Output(" in hint:
                        hint = mld.Output(**potential_kwargs)
                    fn.__annotations__[parameter] = hint
            decorated_command = mld.command_component(**command.component_kwargs)(fn)
            decorated.append(decorated_command)
        return decorated

    def _build_pipeline(self, pipeline: Callable, dec_kwargs: Optional[dict[str, Any]]):
        # Inject the decorated functions
        for f in self.commands:
            pipeline.__globals__[f.__name__] = f
        f = pipeline_dec(**dec_kwargs)(pipeline)
        return pipeline_dec(**dec_kwargs)(pipeline)

    def _setup_dec_kwargs(self, dec_kwargs: dict[str, Any]):
        dec_kwargs["default_compute"] = dec_kwargs.get(
            "default_compute", self.compute.name
        )
        return dec_kwargs

    @override
    def on_run_start(self):
        self.commands = self._register_components(self.commands)
        self.dec_kwargs = self._setup_dec_kwargs(self.dec_kwargs)
        self.pipeline = self._build_pipeline(self.pipeline, self.dec_kwargs)

    @override
    def run(self) -> RunOutput:
        pipeline_job = self.pipeline(**self.inputs, **self.outputs)
        pipe = self.ml_client.jobs.create_or_update(
            pipeline_job, experiment_name=self.experiment_name
        )
        return RunOutput(url=pipe.studio_url)
