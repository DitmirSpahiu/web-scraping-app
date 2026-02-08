import hashlib
import logging
from datetime import datetime
from typing import Dict, List


logger = logging.getLogger(__name__)


def transform_quotes(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Transforms quote records by adding metadata and deduplicating.

    Args:
        records: List of quote record dictionaries.

    Returns:
        Transformed and deduplicated list of records.
    """
    transformed = []
    seen_ids = set()

    for record in records:
        # Add ingested_at
        record['ingested_at'] = datetime.utcnow().isoformat()

        # Add record_id
        key = (record.get('quote_text', '') + record.get('author_name', '')).encode('utf-8')
        record_id = hashlib.sha256(key).hexdigest()
        record['record_id'] = record_id

        # Deduplicate
        if record_id not in seen_ids:
            seen_ids.add(record_id)
            transformed.append(record)
        else:
            logger.info(f"Duplicate record skipped: {record_id}")

    return transformed