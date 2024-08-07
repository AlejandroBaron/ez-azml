# %%
from azure.ai.ml.entities import UsernamePasswordConfiguration, WorkspaceConnection


class DockerWorkspaceConnection(WorkspaceConnection):
    """Azureml connection used for docker environments."""

    def __init__(
        self, username: str, password: str, name: str = "docker_registry", **kwargs
    ):
        credentials = UsernamePasswordConfiguration(
            username=username,
            password=password,
        )
        super().__init__(
            name=name, type="container_registry", credentials=credentials, **kwargs
        )
