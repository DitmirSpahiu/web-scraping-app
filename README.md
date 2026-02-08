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

Details about scraping from https://quotes.toscrape.com.

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