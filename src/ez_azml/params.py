from dataclasses import dataclass

from ez_azml import env


@dataclass
class DockerParams:
    """Dataclass representing a docker setup.

    Args:
        image_name: name of the image, without registry or tag.
        Defaults to env DOCKER_IMAGE
        registry: registry hosting the image. Defaults to env DOCKER_REGISTRY
        tag: image tag. Defaults to env DOCKER_TAG if set, "latest" otherwise
        username: username to log in to the registry. Defaults to env DOCKER_USERNAME
        password: password to log in to the registry. Defaults to env DOCKER_PASSWORD
    """

    image_name: str = env.os_field(env.DOCKER_IMAGE)  # noqa: RUF009
    registry: str = env.os_field(env.DOCKER_REGISTRY)  # noqa: RUF009
    tag: str = env.os_field(env.DOCKER_TAG, "latest")  # noqa: RUF009
    username: str = env.os_field(env.DOCKER_USERNAME)  # noqa: RUF009
    password: str = env.os_field(env.DOCKER_PASSWORD)  # noqa: RUF009

    @property
    def image(self) -> str:
        """Concatenated registry + image name + tag."""
        image = f"{self.image_name}:{self.tag}"
        if self.registry:
            image = f"{self.registry}/{image}"
        return image
