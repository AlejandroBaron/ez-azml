import io
from pathlib import Path
from typing import Any, Optional, Union

import yaml
from azure.ai.ml import Input, MLClient, Output, command, load_component
from azure.ai.ml.entities import Command, UserIdentityConfiguration, WorkspaceConnection
from typing_extensions import override

from ez_azml.cloud_runs.cloud_run import CloudRun, RunOutput


class CommandRun(CloudRun):
    """Cloud run that is based on AzureML Commands.

    Args:
        code: location of the python scripts to use
        commands: commands to run on the cloud (e.g. `python my_script.py`)
        flags: flags to use with the last command.
        identity: credentials to use.
        name: command's name.
        register_kwargs: kwargs to use when registering component.
    """

    def __init__(
        self,
        code: Union[str, Path],
        commands: Union[str, list[str]],
        ws_connection: Optional[WorkspaceConnection] = None,
        flags: Optional[list[str]] = None,
        identity: Optional[UserIdentityConfiguration] = None,
        name: Optional[str] = None,
        register_kwargs: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.ws_connection = ws_connection
        self.identity = identity or UserIdentityConfiguration()
        if isinstance(commands, str):
            commands = [commands]
        if flags:
            commands[-1] += " " + " ".join(flags)
        self.commands = commands
        self.code = Path(code)
        self.name = name or self.code.stem
        self.register_kwargs = register_kwargs or {}

    @property
    def cli_command(self) -> str:
        """Actual cli command run on AzureML."""
        return ";".join(self.commands)

    @property
    def command(self) -> Command:
        """Runnable command."""
        return command(
            command=self.cli_command,
            code=self.code,
            environment=self.environment,
            compute=self.compute.name,
            inputs=self.inputs,
            outputs=self.outputs,
            identity=self.identity,
        )

    def _get_io_dict(
        self, ios: dict[str, Union[Input, Output]], keys: Optional[list[str]] = None
    ):
        ios_as_dict = {}
        keys = keys or ["type"]
        for key, io_obj in ios.items():
            io_d = dict(io_obj)
            ios_as_dict[key] = {k: io_d[k] for k in keys if io_d[k] is not None}
        return ios_as_dict

    def _get_component_yaml_stream(
        self, name: Optional[str] = None, environment: Optional[str] = None, **kwargs
    ) -> io.StringIO:
        inputs_dict = self._get_io_dict(self.inputs)
        outputs_dict = self._get_io_dict(self.outputs)
        if not environment:
            self.ml_client.environments.create_or_update(self.environment)
            version = self.environment.version or 1
            environment = f"azureml:{self.environment.name}:{version}"
        yaml_dict = {
            "name": name or self.name,
            "inputs": inputs_dict,
            "outputs": outputs_dict,
            "code": str(self.code),
            "command": self.cli_command,
            "environment": environment,
            **kwargs,
        }
        yaml_stream = io.StringIO()
        yaml.dump(yaml_dict, yaml_stream)
        yaml_stream.seek(0)  # Move the file pointer to the beginning
        return yaml_stream

    def get_component(self, **kwargs):
        """Returns the mldesigner component."""
        yaml_file = self._get_component_yaml_stream(**self.register_kwargs, **kwargs)
        return load_component(yaml_file)

    @override
    def register(self, ml_client: Optional[MLClient] = None, **kwargs):
        ml_client = ml_client or self.ml_client
        component = self.get_component(**kwargs)
        ml_client.components.create_or_update(component)
        return component

    @override
    def run(self) -> str:
        if self.ws_connection:
            self.ml_client.connections.create_or_update(self.ws_connection)
        self.ml_client.begin_create_or_update(self.compute).result()
        cloud_job = self.ml_client.create_or_update(self.command)
        return RunOutput(url=cloud_job.studio_url)
