from ez_azml.entities import DockerEnvironment, DockerWorkspaceConnection
from ez_azml.params import DockerParams

from .command import Command


class DockerCommand(Command):
    """A Command that uses a docker image.

    Args:
        docker: docker params representing the image to use
    """

    def __init__(self, docker: DockerParams, **kwargs) -> None:
        registry = docker.registry
        ws_connection = None
        if registry and docker.username and docker.password:
            ws_connection = DockerWorkspaceConnection(
                username=docker.username,
                password=docker.password,
                target=registry,
            )
        environment = DockerEnvironment(docker=docker)
        super().__init__(environment=environment, ws_connection=ws_connection, **kwargs)
