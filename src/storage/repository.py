import json
import os
import tempfile
from typing import Dict, List


def ensure_dir(path: str) -> None:
    """
    Ensures the directory for the given path exists.

    Args:
        path: The file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_jsonl(path: str, records: List[Dict[str, str]]) -> None:
    """
    Saves records to a JSONL file atomically.

    Args:
        path: The output file path.
        records: List of record dictionaries.
    """
    ensure_dir(path)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=os.path.dirname(path), delete=False, suffix='.tmp') as tmp:
            temp_path = tmp.name
            for record in records:
                json.dump(record, tmp, separators=(',', ':'))
                tmp.write('\n')
            tmp.flush()
            os.fsync(tmp.fileno())
        os.rename(temp_path, path)
    except Exception:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise