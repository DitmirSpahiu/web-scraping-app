import logging
from typing import NoReturn


def setup_logging() -> None:
    """
    Sets up logging with a clean formatter.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )