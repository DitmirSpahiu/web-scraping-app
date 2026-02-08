import logging
import re
from typing import Dict, List


logger = logging.getLogger(__name__)


def clean_quote_record(record: Dict[str, str]) -> Dict[str, str]:
    """
    Cleans and normalizes a quote record.

    Args:
        record: The raw quote record dictionary.

    Returns:
        The cleaned record dictionary.
    """
    cleaned = record.copy()

    # Normalize whitespace for quote_text
    if 'quote_text' in cleaned and cleaned['quote_text']:
        cleaned['quote_text'] = re.sub(r'\s+', ' ', cleaned['quote_text'].strip())

    # Normalize whitespace for author_description
    if 'author_description' in cleaned and cleaned['author_description']:
        cleaned['author_description'] = re.sub(r'\s+', ' ', cleaned['author_description'].strip())

    # Ensure tags are lowercase and unique
    if 'tags' in cleaned and isinstance(cleaned['tags'], list):
        cleaned['tags'] = list(set(tag.lower().strip() for tag in cleaned['tags'] if tag.strip()))

    # Ensure URLs are clean strings
    for url_field in ['author_url', 'page_url']:
        if url_field in cleaned and cleaned[url_field]:
            cleaned[url_field] = cleaned[url_field].strip()

    return cleaned