# QuoteHarvester

## Overview

QuoteHarvester is a modular data pipeline project that scrapes quotes from https://quotes.toscrape.com and enriches them with author details by visiting each author page.

## Configuration

Environment variables (optional, defaults provided):

- `TIMEOUT_SECONDS`: Request timeout in seconds (default: 10)
- `MAX_RETRIES`: Maximum number of retries for failed requests (default: 3)
- `OUTPUT_DIR`: Directory for output files (default: "data/processed")

## Architecture

Describe the modular architecture here.

## Data Flow

Describe the data flow here.

## Scraping Details

Scraping is performed from https://quotes.toscrape.com using a custom HTTP client with:
- User-Agent header for polite scraping
- Configurable timeouts (default 10 seconds)
- Exponential backoff retries for timeouts and 5xx errors (up to 3 retries)
- Proper error handling for 4xx client errors (raising FetchError except for 429 Too Many Requests)

From list pages, the following fields are extracted for each quote:
- quote_text: The quote content (curly quotes stripped)
- author_name: The author's name
- tags: List of associated tags
- author_url: Absolute URL to the author's detail page
- page_url: The URL of the page where the quote was found

## Enrichment (Author Pages)

Details about enriching with author details.

## Security

Security measures including Fernet encryption and SHA-256 hashing.

## Outputs

JSONL files for processed records and invalid records.

## How to Run

Steps to run the pipeline.

## Testing

Testing information.

## Git History

Git history details.