from typing import Optional

from azure.ai.ml.entities import Environment

from ez_azml.params import DockerParams


class DockerEnvironment(Environment):
    """Enviromment for training that uses a docker image.

    Args:
        docker: docker image's parameters
        name: environment's name.
        description: environment's description
    """

    def __init__(
        self,
        docker: DockerParams,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs,
    ):
        name = name or f"{docker.image_name}-env-{docker.tag.replace('.','_')}".replace(
            "/", "-"
        )
        description = (
            description or f"{docker.image_name} Docker Command Job environment"
        )
        super().__init__(
            image=docker.image, name=name, description=description, **kwargs
        )
