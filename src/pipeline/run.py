import argparse
import logging
import os
from typing import Dict, List

from src.config.logging import setup_logging
from src.config.settings import OUTPUT_DIR
from src.processing.clean import clean_quote_record
from src.processing.transform import transform_quotes
from src.processing.validate import validate_quotes
from src.scraping.author_parser import parse_author_page
from src.scraping.client import HttpClient
from src.scraping.parser import find_next_page_url, parse_quotes_page
from src.security.crypto import protect_record
from src.storage.repository import save_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the QuoteHarvester data pipeline: scrape quotes, enrich with author details, process, and save to JSONL files.')
    parser.add_argument('--max-pages', type=int, default=3, help='Maximum number of quote list pages to scrape from https://quotes.toscrape.com (default: 3)')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR, help='Directory to save processed quotes.jsonl and invalid.jsonl files (default: data/processed)')
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    client = HttpClient()
    base_url = 'https://quotes.toscrape.com'
    page_url = base_url
    pages_scraped = 0
    all_quotes: List[Dict[str, str]] = []
    author_cache: Dict[str, Dict[str, str]] = {}

    # Scrape pages
    while page_url and pages_scraped < args.max_pages:
        logger.info(f"Scraping page {pages_scraped + 1}: {page_url}")
        try:
            html = client.fetch(page_url)
            quotes = parse_quotes_page(html, page_url)
            all_quotes.extend(quotes)
            page_url = find_next_page_url(html, page_url)
            pages_scraped += 1
        except Exception as e:
            logger.error(f"Failed to scrape {page_url}: {e}, skipping to next page if available")
            page_url = None  # Stop scraping on failure to avoid infinite loops

    logger.info(f"Pages scraped: {pages_scraped}, Quotes parsed: {len(all_quotes)}")

    # Fetch unique authors
    unique_authors = set(q['author_url'] for q in all_quotes if q.get('author_url'))
    authors_fetched = 0
    for url in unique_authors:
        logger.info(f"Fetching author: {url}")
        try:
            html = client.fetch(url)
            author_data = parse_author_page(html, url)
            author_cache[url] = author_data
            authors_fetched += 1
        except Exception as e:
            logger.warning(f"Failed to fetch author {url}: {e}, setting author fields to None")
            author_cache[url] = {}

    logger.info(f"Authors fetched: {authors_fetched}")

    # Merge author details
    for quote in all_quotes:
        author_url = quote.get('author_url')
        if author_url and author_url in author_cache:
            quote.update(author_cache[author_url])

    # Process records
    cleaned = [clean_quote_record(q) for q in all_quotes]
    valid, invalid = validate_quotes(cleaned)
    transformed = transform_quotes(valid)
    protected = [protect_record(t) for t in transformed]

    # Save outputs
    quotes_path = os.path.join(args.output_dir, 'quotes.jsonl')
    invalid_path = os.path.join(args.output_dir, 'invalid.jsonl')
    save_jsonl(quotes_path, protected)
    save_jsonl(invalid_path, invalid)

    logger.info(f"Valid records saved: {len(protected)} to {quotes_path}")
    logger.info(f"Invalid records saved: {len(invalid)} to {invalid_path}")


if __name__ == '__main__':
    main()