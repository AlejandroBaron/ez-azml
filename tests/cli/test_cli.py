from unittest import mock

import pytest
from ez_azml.cli import EzAzureMLCLI


@pytest.mark.parametrize("command", ["run", "register"])
def test_cloud_run_hooks_call(command: str):
    """Tests that cli is calling pre and post hooks."""
    mock_cloud_run = mock.MagicMock()
    cli = EzAzureMLCLI(cloud_run=mock_cloud_run)

    getattr(cli, command)()

    expected = [f"on_{command}_start", command, f"on_{command}_end"]
    for method in expected:
        getattr(mock_cloud_run, method).assert_called_once()


def test_ml_client_set():
    """Tests that ml_client is injected."""
    mock_cloud_run = mock.MagicMock()
    mock_cloud_run.ml_client = None
    cli = EzAzureMLCLI(cloud_run=mock_cloud_run)
    assert cli.ml_client == mock_cloud_run.ml_client
