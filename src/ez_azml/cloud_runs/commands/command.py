from typing import Optional

from azure.ai.ml import command
from azure.ai.ml.entities import (
    UserIdentityConfiguration,
    WorkspaceConnection,
)
from typing_extensions import override

from ez_azml.cloud_runs.cloud_run import CloudRun, RunOutput


class Command(CloudRun):
    """Cloud run that is based on AzureML Commands.

    Args:
        code: location of the scripts to use
        commands: commands to run on the cloud (e.g. `python my_script.py`)
        flags: flags to use with the last command.
        identity: credentials to use.
    """

    def __init__(
        self,
        code: str,
        commands: list[str],
        ws_connection: Optional[WorkspaceConnection] = None,
        flags: Optional[list[str]] = None,
        identity: Optional[UserIdentityConfiguration] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.ws_connection = ws_connection
        identity = identity or UserIdentityConfiguration()
        if flags:
            commands[-1] += " " + " ".join(flags)
        self.job = command(
            command=";".join(commands),
            code=code,
            environment=self.environment,
            compute=self.compute.name,
            inputs=self.inputs,
            outputs=self.outputs,
            identity=identity,
        )

    @override
    def run(self) -> str:
        if self.ws_connection:
            self.ml_client.connections.create_or_update(self.ws_connection)
        self.ml_client.environments.create_or_update(self.environment)
        self.ml_client.begin_create_or_update(self.compute).result()
        cloud_job = self.ml_client.create_or_update(self.job)
        return RunOutput(url=cloud_job.studio_url)
