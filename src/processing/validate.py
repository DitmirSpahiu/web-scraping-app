import logging
from typing import Dict, List, Tuple


logger = logging.getLogger(__name__)


def validate_quotes(records: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    Validates quote records for required fields.

    Args:
        records: List of quote record dictionaries.

    Returns:
        A tuple of (valid_records, invalid_records).
        Invalid records contain 'errors' list and 'record' dict.
    """
    required_fields = ['quote_text', 'author_name', 'author_url']
    valid = []
    invalid = []

    for record in records:
        errors = []
        for field in required_fields:
            if field not in record or not record[field] or not record[field].strip():
                errors.append(f"Missing or empty {field}")

        if errors:
            invalid.append({
                'errors': errors,
                'record': record
            })
            logger.warning(f"Invalid record: {errors}")
        else:
            valid.append(record)

    return valid, invalid