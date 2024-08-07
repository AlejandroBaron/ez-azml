import os
from dataclasses import field
from typing import Optional

DOCKER_REGISTRY = "DOCKER_REGISTRY"
DOCKER_USERNAME = "DOCKER_USERNAME"
DOCKER_PASSWORD = "DOCKER_PASSWORD"  # noqa: S105
DOCKER_REGISTRY = "DOCKER_REGISTRY"
DOCKER_TAG = "DOCKER_TAG"
DOCKER_IMAGE = "DOCKER_IMAGE"


def os_field(env_var: str, default: Optional[str] = None) -> Optional[str]:
    """Dataclass field that retrieves an environment variable.

    Args:
        env_var: variable to try to retrive.
        default: value to use if env variable was not set
    """
    return field(default_factory=lambda: os.getenv(env_var, default))
