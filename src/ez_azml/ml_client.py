# %%
import os
from typing import Any, Optional

from azure.ai.ml import MLClient
from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential


class EzMLClient(MLClient):
    """A easy client class to interact with Azure ML services.

    Args:
        credential: The credential to use for authentication.
        Defaults to DefaultAzureCredential()
        subscription_id: The Azure subscription ID.
        Defaults to env AZURE_SUBSCRIPTION_ID.
        resource_group_name: The Azure resource group.
        Defaults to env AZURE_RESOURCE_GROUP_NAME.
        workspace_name: The workspace to use in the client.
        Defaults to env AZURE_WORKSPACE.
    """

    def __init__(
        self,
        credential: Optional[TokenCredential] = None,
        subscription_id: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        workspace_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        credential = credential or DefaultAzureCredential()
        subscription_id = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID")
        resource_group_name = resource_group_name or os.getenv(
            "AZURE_RESOURCE_GROUP_NAME"
        )
        workspace_name = workspace_name or os.getenv("AZURE_WORKSPACE")
        super().__init__(
            credential, subscription_id, resource_group_name, workspace_name, **kwargs
        )
