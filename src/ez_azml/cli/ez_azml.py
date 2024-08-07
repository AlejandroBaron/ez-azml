from typing import Optional

from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
from loguru import logger

from ez_azml.cloud_runs.cloud_run import CloudRun
from ez_azml.ml_client import EzMLClient


class EzAzureMLCLI:
    """CLI class.

    Contains commands and interactions

    Args:
        cloud_run: object representing a cloud run
        ml_client: client used for cloud interactions.
            Will be injected on to the cloud_run if it's lacking one
        compute: cluster used to run the `cloud_run`.
            Will be injected on to the cloud_run if it's lacking one
    """

    def __init__(
        self,
        cloud_run: Optional[CloudRun] = None,
        ml_client: Optional[MLClient] = None,
        compute: Optional[AmlCompute] = None,
    ):
        self.cloud_run = cloud_run
        self.ml_client = ml_client or EzMLClient()
        self.compute = compute

        self.cloud_run.ml_client = self.cloud_run.ml_client or self.ml_client
        self.cloud_run.compute = self.cloud_run.compute or self.compute

    def run(self):
        """Runs the cloud run.

        Calls the object's `on_run_start` and `on_run_end` hooks
        """
        self.cloud_run.on_run_start()
        output = self.cloud_run.run()
        logger.info(f"Run available at {output.url}")
        self.cloud_run.on_run_end(output)
