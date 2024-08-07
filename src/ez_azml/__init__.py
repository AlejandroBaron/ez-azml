from ez_azml.entities.compute import Cluster, SpotCluster
from ez_azml.entities.workspace import DockerWorkspaceConnection
from ez_azml.ml_client import EzMLClient

__all__ = ["EzMLClient", "SpotCluster", "Cluster", "DockerWorkspaceConnection"]
