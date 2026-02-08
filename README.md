# QuoteHarvester

## Overview

QuoteHarvester is a modular data pipeline project that scrapes quotes from https://quotes.toscrape.com and enriches them with author details by visiting each author page.

## Configuration

Environment variables (optional, defaults provided):

- `TIMEOUT_SECONDS`: Request timeout in seconds (default: 10)
- `MAX_RETRIES`: Maximum number of retries for failed requests (default: 3)
- `OUTPUT_DIR`: Directory for output files (default: "data/processed")

## Architecture

The project follows a modular architecture with the following components:

- **Scraping**: Handles HTTP requests, HTML parsing for quotes and author pages
- **Processing**: Cleans, validates, transforms, and deduplicates data
- **Security**: Manages encryption, hashing, and environment secrets
- **Storage**: Provides atomic JSONL file writing
- **Pipeline**: Orchestrates the end-to-end data flow with CLI interface

## Data Flow

Data flows through the following numbered stages:

1. **Scraping**: Iterate through list pages using "Next" links, parse quotes with CSS selectors (e.g., div.quote, span.text, small.author)
2. **Enrichment**: Fetch unique author pages once (cached), merge author details into quote records
3. **Processing**: Clean whitespace/tags, validate required fields, add metadata (record_id, ingested_at), deduplicate
4. **Security**: Encrypt sensitive fields (author_description) using Fernet
5. **Storage**: Save valid records to quotes.jsonl, invalid to invalid.jsonl atomically

## Scraping Details

Scraping uses CSS selectors for robust parsing:
- Quotes: `div.quote` containers
- Text: `span.text`
- Author: `small.author`
- Tags: `div.tags a.tag`
- Author URL: `a` with href
- Next page: `li.next a`

Resilience: Custom HTTP client with User-Agent, timeouts, exponential backoff retries for 5xx/429, graceful error handling for 4xx (except 429).

## Enrichment (Author Pages)

Author pages are cached per unique URL to avoid redundant fetches. Merged fields include:
- author_birth_date
- author_birth_location
- author_description

## Security

Environment-based key management: FERNET_KEY loaded from .env via python-dotenv. No hardcoded secrets.

Encrypted at rest: author_description field encrypted with Fernet before storage.

## Outputs

- `data/processed/quotes.jsonl`: Valid records, e.g., `{"quote_text":"Test","author_name":"Author","record_id":"abc123","ingested_at":"2026-02-08T12:00:00"}`
- `data/processed/invalid.jsonl`: Invalid records, e.g., `{"errors":["Missing author_name"],"record":{"quote_text":"Test"}}`

## How to Run

1. Generate Fernet key: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
2. Copy `.env.example` to `.env`, set `FERNET_KEY` to the generated key
3. Install: `pip install -r requirements.txt`
4. Run: `python -m src.pipeline.run --max-pages 3 --output-dir data/processed`

## Testing

Run tests with `pytest -q`. Tests cover parsing quotes and author pages from sample HTML, and crypto encrypt/decrypt roundtrip (skipped if FERNET_KEY not set).

## Git History

Git history details.