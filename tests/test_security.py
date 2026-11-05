"""Tests for PIN hashing."""

import unittest

from atm.security import generate_salt, hash_pin, verify_pin
from tests.helpers import TEST_PIN


class PinHashingTests(unittest.TestCase):
    def test_hash_is_deterministic_for_the_same_salt(self):
        salt = generate_salt()
        self.assertEqual(hash_pin(TEST_PIN, salt), hash_pin(TEST_PIN, salt))

    def test_different_salts_produce_different_hashes(self):
        self.assertNotEqual(
            hash_pin(TEST_PIN, generate_salt()), hash_pin(TEST_PIN, generate_salt())
        )

    def test_verify_pin_accepts_the_correct_pin(self):
        salt = generate_salt()
        self.assertTrue(verify_pin(TEST_PIN, salt, hash_pin(TEST_PIN, salt)))

    def test_verify_pin_rejects_a_wrong_pin(self):
        salt = generate_salt()
        self.assertFalse(verify_pin("0000", salt, hash_pin(TEST_PIN, salt)))


if __name__ == "__main__":
    unittest.main()
