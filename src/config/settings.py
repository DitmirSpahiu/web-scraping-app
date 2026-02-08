import os
from typing import Any


# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env


# Default settings
TIMEOUT_SECONDS: int = int(os.getenv('TIMEOUT_SECONDS', 10))
MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', 3))
OUTPUT_DIR: str = os.getenv('OUTPUT_DIR', 'data/processed')