from unittest import mock

import pytest
from ez_azml.params import DockerParams  # Replace with the actual import path

from tests.utils import mock_env_vars, mock_os_getenv


@pytest.mark.parametrize(
    "kwargs",
    [
        ({}),
        (
            {
                "image_name": "custom_image",
                "registry": "custom_registry",
                "tag": "custom_tag",
                "username": "custom_username",
                "password": "custom_password",
            }
        ),
        ({"image_name": "custom_image", "registry": "custom_registry"}),
        ({"image_name": "custom_image", "tag": "custom_tag"}),
        ({"image_name": "custom_image", "registry": "", "tag": "custom_tag"}),
    ],
)
@mock.patch("os.getenv", side_effect=mock_os_getenv)
def test_docker_params(mock_os_getenv, kwargs):
    """Tests docker params constructor."""
    # Initialize DockerParams with the given kwargs
    params = DockerParams(**kwargs)

    # Derive expected values based on kwargs or mock_env_vars
    expected_image_name = kwargs.get("image_name", mock_env_vars["DOCKER_IMAGE"])
    expected_registry = kwargs.get("registry", mock_env_vars["DOCKER_REGISTRY"])
    expected_tag = kwargs.get("tag", mock_env_vars["DOCKER_TAG"])
    expected_username = kwargs.get("username", mock_env_vars["DOCKER_USERNAME"])
    expected_password = kwargs.get("password", mock_env_vars["DOCKER_PASSWORD"])

    # Build the expected image string
    if expected_registry:
        expected_image = f"{expected_registry}/{expected_image_name}:{expected_tag}"
    else:
        expected_image = f"{expected_image_name}:{expected_tag}"

    # Assertions
    assert params.image_name == expected_image_name
    assert params.registry == expected_registry
    assert params.tag == expected_tag
    assert params.username == expected_username
    assert params.password == expected_password
    assert params.image == expected_image
