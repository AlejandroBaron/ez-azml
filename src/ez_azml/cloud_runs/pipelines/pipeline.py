from typing import Any, Callable, Optional

from azure.ai.ml.dsl import pipeline as pipeline_dec
from azure.ai.ml.entities import Component
from typing_extensions import override

from ez_azml.cloud_runs.cloud_run import CloudRun, RunOutput
from ez_azml.cloud_runs.commands import CommandRun


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
        commands: dict[str, CommandRun],
        pipeline: Callable,
        dec_kwargs: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.experiment_name = experiment_name
        if isinstance(commands, CommandRun):
            commands = [commands]
        if isinstance(commands, list):
            commands = {command.name: command for command in commands}
        self.commands = commands
        self.dec_kwargs = dec_kwargs or {}
        self.pipeline = pipeline

    def _register_components(self, commands: dict[str, CommandRun]) -> list[Component]:
        return [command.register(self.ml_client) for command in commands.values()]

    def _build_pipeline(
        self,
        pipeline: Callable,
        dec_kwargs: Optional[dict[str, Any]],
        components: list[Component],
    ):
        # Inject the components
        for component in components:
            pipeline.__globals__[component.name] = component
        dec_pipeline = pipeline_dec(**dec_kwargs)(pipeline)
        # for component in components:
        #     dec_pipeline.__globals__[component.name] = component
        return dec_pipeline

    def _setup_dec_kwargs(self, dec_kwargs: dict[str, Any]):
        if self.compute:
            dec_kwargs["default_compute"] = dec_kwargs.get(
                "default_compute", self.compute.name
            )
        if self.environment:
            # TODO: check correct key
            dec_kwargs["environment"] = dec_kwargs.get("environment", self.environment)
        return dec_kwargs

    @override
    def register(self):
        return self.ml_client.jobs.create_or_update(
            self.pipeline_job, experiment_name=self.experiment_name
        )

    @override
    def on_run_start(self):
        self.components = self._register_components(self.commands)
        self.dec_kwargs = self._setup_dec_kwargs(self.dec_kwargs)
        self.pipeline = self._build_pipeline(
            self.pipeline, self.dec_kwargs, self.components
        )

    @override
    def run(self) -> RunOutput:
        self.pipeline_job = self.pipeline(**self.inputs, **self.outputs)
        pipe = self.register()
        return RunOutput(url=pipe.studio_url)
