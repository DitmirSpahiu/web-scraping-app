import hashlib
from typing import Dict

from cryptography.fernet import Fernet

from src.security.secrets import get_env


# Initialize Fernet with key from environment
key = get_env('FERNET_KEY')
fernet = Fernet(key.encode())


def encrypt_value(value: str) -> str:
    """
    Encrypts a string value using Fernet.

    Args:
        value: The string to encrypt.

    Returns:
        The encrypted string.
    """
    return fernet.encrypt(value.encode()).decode()


def decrypt_value(encrypted: str) -> str:
    """
    Decrypts a string value using Fernet.

    Args:
        encrypted: The encrypted string.

    Returns:
        The decrypted string.
    """
    return fernet.decrypt(encrypted.encode()).decode()


def sha256_hex(value: str) -> str:
    """
    Computes the SHA-256 hex digest of a string.

    Args:
        value: The string to hash.

    Returns:
        The hex digest.
    """
    return hashlib.sha256(value.encode()).hexdigest()


def protect_record(record: Dict[str, str], encrypt_quote: bool = False) -> Dict[str, str]:
    """
    Protects a record by encrypting sensitive fields.

    Args:
        record: The record dictionary.
        encrypt_quote: Whether to also encrypt quote_text.

    Returns:
        The protected record with encrypted fields.
    """
    protected = record.copy()
    if 'author_description' in protected and protected['author_description']:
        protected['author_description'] = encrypt_value(protected['author_description'])
    if encrypt_quote and 'quote_text' in protected and protected['quote_text']:
        protected['quote_text'] = encrypt_value(protected['quote_text'])
    return protected