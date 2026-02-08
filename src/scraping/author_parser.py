import logging
from typing import Dict, Optional

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def parse_author_page(html: str, author_url: str) -> Dict[str, Optional[str]]:
    """
    Parses the HTML of an author detail page and extracts author data.

    Args:
        html: The HTML content of the author page.
        author_url: The URL of the author page.

    Returns:
        A dictionary containing author information.
    """
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'author_name': None,
        'author_birth_date': None,
        'author_birth_location': None,
        'author_description': None,
        'author_url': author_url
    }

    # Extract author name
    name_elem = soup.find('h3', class_='author-title')
    if name_elem:
        data['author_name'] = name_elem.get_text().strip()
    else:
        logger.warning(f"Missing author name in {author_url}")

    # Extract birth details
    details_elem = soup.find('p', class_='author-details')
    if details_elem:
        text = details_elem.get_text()
        # Assuming format: "Born: date in location"
        if 'Born:' in text:
            parts = text.replace('Born:', '').strip().split(' in ')
            if len(parts) >= 1:
                data['author_birth_date'] = parts[0].strip()
            if len(parts) >= 2:
                data['author_birth_location'] = parts[1].strip()
        else:
            logger.warning(f"Unexpected birth details format in {author_url}")
    else:
        logger.warning(f"Missing author details in {author_url}")

    # Extract description
    desc_elem = soup.find('div', class_='author-description')
    if desc_elem:
        data['author_description'] = desc_elem.get_text().strip()
    else:
        logger.warning(f"Missing author description in {author_url}")

    return data