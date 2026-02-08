import pytest

from src.security.crypto import decrypt_value, encrypt_value


def test_encrypt_decrypt_roundtrip():
    """Test encrypt/decrypt roundtrip, skip if FERNET_KEY not set."""
    try:
        from src.security.secrets import get_env
        get_env('FERNET_KEY')
    except ValueError:
        pytest.skip("FERNET_KEY not set")

    original = "test string for encryption"
    encrypted = encrypt_value(original)
    decrypted = decrypt_value(encrypted)
    assert decrypted == original