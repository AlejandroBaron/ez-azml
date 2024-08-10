from unittest import mock

from ez_azml import EzMLClient
from ez_azml.env import (
    AZURE_RESOURCE_GROUP_NAME,
    AZURE_SUBSCRIPTION_ID,
    AZURE_WORKSPACE,
)

from tests.utils import mock_os_getenv


@mock.patch("os.getenv", side_effect=mock_os_getenv)
def test_ml_client_envs(mock_os_getenv):
    """Tests that init properly retrieves env variables."""
    client = EzMLClient()

    assert client.subscription_id == mock_os_getenv(AZURE_SUBSCRIPTION_ID)
    assert client.resource_group_name == mock_os_getenv(AZURE_RESOURCE_GROUP_NAME)
    assert client.workspace_name == mock_os_getenv(AZURE_WORKSPACE)
