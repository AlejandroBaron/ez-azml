from jsonargparse import CLI, ArgumentParser
from loguru import logger

from ez_azml.cli.ez_azml import EzAzureMLCLI


def main():
    """Actual cli command for the package."""
    try:
        from dotenv import load_dotenv

        logger.debug("package dotenv available. Calling dotenv.load_dotenv()")
        load_dotenv()
    except ImportError:
        pass
    CLI(
        EzAzureMLCLI,
        parser_class=ArgumentParser,
        env_prefix="EZAZML",
        default_env=True,
    )


if __name__ == "__main__":
    main()
