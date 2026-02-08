import logging
import time
from typing import Optional

import requests
from requests.exceptions import RequestException

from src.config.settings import TIMEOUT_SECONDS, MAX_RETRIES


logger = logging.getLogger(__name__)


class FetchError(Exception):
    """Custom exception for fetch errors."""
    pass


class HttpClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'QuoteHarvester/1.0 (https://github.com/username/quoteharvester)'
        })

    def fetch(self, url: str) -> str:
        """
        Fetches the content of a URL with retries and error handling.

        Args:
            url: The URL to fetch.

        Returns:
            The response text.

        Raises:
            FetchError: For 4xx errors (except 429).
        """
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = self.session.get(url, timeout=TIMEOUT_SECONDS)
                if response.status_code == 200:
                    return response.text
                elif 400 <= response.status_code < 500:
                    if response.status_code == 429:
                        # Too many requests, retry
                        logger.warning(f"429 Too Many Requests for {url}, retrying...")
                    else:
                        raise FetchError(f"Client error {response.status_code} for {url}")
                elif 500 <= response.status_code < 600:
                    logger.warning(f"Server error {response.status_code} for {url}, retrying...")
                else:
                    logger.warning(f"Unexpected status {response.status_code} for {url}, retrying...")
            except RequestException as e:
                logger.warning(f"Request failed for {url}: {e}, retrying...")

            if attempt < MAX_RETRIES:
                backoff = 2 ** attempt
                logger.info(f"Retrying {url} in {backoff} seconds...")
                time.sleep(backoff)

        raise FetchError(f"Failed to fetch {url} after {MAX_RETRIES + 1} attempts")