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

Security measures including Fernet encryption and SHA-256 hashing.

## Outputs

Processed records are saved to JSONL files in the output directory, including metadata:
- record_id: Unique SHA-256 hash of quote_text + author_name for deduplication
- ingested_at: UTC ISO timestamp of when the record was processed

Invalid records (failing validation for required fields: quote_text, author_name, author_url) are saved to a separate JSONL file with error details and the original record.

## How to Run

Steps to run the pipeline.

## Testing

Testing information.

## Git History

Git history details.