import os
from typing import Optional

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def get_env(name: str, required: bool = True, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieves an environment variable.

    Args:
        name: The name of the environment variable.
        required: Whether the variable is required.
        default: Default value if not set.

    Returns:
        The value of the environment variable.

    Raises:
        ValueError: If required and not set.
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"Required environment variable {name} not set")
    return value