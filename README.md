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

Data flows through the following stages:
1. Scraping: Fetch quotes list pages and author detail pages
2. Processing: Clean and normalize extracted data, validate records, transform by adding metadata (record_id: SHA-256 hash of quote_text + author_name, ingested_at: UTC ISO timestamp), and deduplicate by record_id
3. Enrichment: Merge author details into quote records
4. Storage: Save processed records to JSONL files

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

Author pages are visited to enrich quotes with additional author details. The following fields are extracted:
- author_name: The author's full name
- author_birth_date: Birth date (if available)
- author_birth_location: Birth location (if available)
- author_description: Biographical description
- author_url: The URL of the author page

Missing fields are set to None and logged as warnings.

## Security

Security measures include Fernet encryption and SHA-256 hashing.
To set up security:
1. Copy `.env.example` to `.env`
2. Generate a Fernet key: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
3. Set `FERNET_KEY` in `.env` to the generated key
Environment variables are loaded using python-dotenv, with no hardcoded secrets.

Data is encrypted at rest: author_description is encrypted using Fernet before storage. Optionally, quote_text can also be encrypted.

## Outputs

Processed records are saved to JSONL files in the output directory, including metadata:
- record_id: Unique SHA-256 hash of quote_text + author_name for deduplication
- ingested_at: UTC ISO timestamp of when the record was processed

Invalid records (failing validation for required fields: quote_text, author_name, author_url) are saved to a separate JSONL file with error details and the original record.

Output files:
- `data/processed/quotes.jsonl`: Valid processed quotes in JSONL format
- `data/processed/invalid.jsonl`: Invalid records with errors in JSONL format

## How to Run

Steps to run the pipeline.

## Testing

Testing information.

## Git History

Git history details.