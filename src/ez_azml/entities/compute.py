# %%
from typing import ClassVar

from azure.ai.ml.entities import AmlCompute


class Cluster(AmlCompute):
    """AzureML Compute resource with some aliases for size.

    See Cluster.size_aliases
    """

    size_aliases: ClassVar[dict] = {
        "T4": "Standard_NC4as_T4_v3",
        "V100": "Standard_NC6s_v3",
        "CPU": "Standard_D1_v2",
    }

    def __init__(self, size: str, idle_time_before_scale_down: int = 5, **kwargs):
        size = self.size_aliases.get(size, size)
        super().__init__(
            size=size,
            idle_time_before_scale_down=idle_time_before_scale_down,
            **kwargs,
        )


class SpotCluster(Cluster):
    """Cluster that can be preempted."""

    def __init__(self, **kwargs):
        super().__init__(
            tier="low_priority",
            **kwargs,
        )
