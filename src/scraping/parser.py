import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def parse_quotes_page(html: str, page_url: str) -> List[Dict[str, str]]:
    """
    Parses the HTML of a quotes page and extracts quote data.

    Args:
        html: The HTML content of the page.
        page_url: The URL of the page.

    Returns:
        A list of dictionaries, each containing quote data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []

    for quote_div in soup.find_all('div', class_='quote'):
        try:
            # Extract quote text
            quote_text_elem = quote_div.find('span', class_='text')
            if not quote_text_elem:
                logger.warning(f"Missing quote text in {page_url}")
                continue
            quote_text = quote_text_elem.get_text().strip()
            # Strip curly quotes
            quote_text = quote_text.strip('"').strip('“').strip('”')

            # Extract author name
            author_elem = quote_div.find('small', class_='author')
            if not author_elem:
                logger.warning(f"Missing author in {page_url}")
                continue
            author_name = author_elem.get_text().strip()

            # Extract tags
            tags = []
            tags_div = quote_div.find('div', class_='tags')
            if tags_div:
                tag_links = tags_div.find_all('a', class_='tag')
                tags = [tag.get_text().strip() for tag in tag_links]

            # Extract author URL
            author_link = quote_div.find('a', href=True)
            if not author_link:
                logger.warning(f"Missing author link in {page_url}")
                continue
            author_url = urljoin(page_url, author_link['href'])

            quotes.append({
                'quote_text': quote_text,
                'author_name': author_name,
                'tags': tags,
                'author_url': author_url,
                'page_url': page_url
            })

        except Exception as e:
            logger.warning(f"Error parsing quote block in {page_url}: {e}")
            continue

    return quotes


def find_next_page_url(html: str, current_url: str) -> Optional[str]:
    """
    Finds the URL of the next page from the HTML.

    Args:
        html: The HTML content of the page.
        current_url: The current page URL.

    Returns:
        The absolute URL of the next page, or None if not found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find('li', class_='next')
    if next_link:
        a_tag = next_link.find('a', href=True)
        if a_tag:
            return urljoin(current_url, a_tag['href'])
    return None