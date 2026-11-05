"""PIN hashing helpers.

The simulation stores the PIN as a salted SHA-256 hash instead of plain
text and compares hashes in constant time -- the same pattern a real
system would follow with a slower KDF such as bcrypt or argon2.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

SALT_BYTES = 16


def generate_salt() -> str:
    """Return a random hex string used to salt a PIN hash."""
    return secrets.token_hex(SALT_BYTES)


def hash_pin(pin: str, salt: str) -> str:
    """Hash ``pin`` together with ``salt`` using SHA-256."""
    return hashlib.sha256((salt + pin).encode("utf-8")).hexdigest()


def verify_pin(pin: str, salt: str, expected_hash: str) -> bool:
    """Return True if ``pin`` matches ``expected_hash`` (constant time)."""
    return hmac.compare_digest(hash_pin(pin, salt), expected_hash)
