from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from azure.ai.ml import Input, MLClient, Output
from azure.ai.ml.entities import AmlCompute, Environment


@dataclass
class RunOutput:
    """Output info for a CloudRun."""

    url: str


class CloudRun(ABC):
    """Abstract class representing any process that runs on the cloud.

    Args:
        compute: Compute used to execute the run
        environment: Environment used to host the run
        ml_client: Client in charge of interacting with the cloud provider
    """

    def __init__(
        self,
        compute: Optional[AmlCompute] = None,
        environment: Optional[Environment] = None,
        ml_client: Optional[MLClient] = None,
        inputs: Optional[dict[str, Input]] = None,
        outputs: Optional[dict[str, Output]] = None,
    ) -> None:
        self.compute = compute
        self.environment = environment
        self.ml_client = ml_client
        self.inputs = inputs or {}
        self.outputs = outputs or {}

    def on_run_start(self):
        """Hook called before run is submitted."""
        return

    @abstractmethod
    def run(self) -> RunOutput:
        """Submits and runs the job."""

    def on_run_end(self, output: RunOutput):
        """Hook called once run has been submitted."""
        return
