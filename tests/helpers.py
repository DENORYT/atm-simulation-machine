"""Shared factories for the test suite."""

from decimal import Decimal

from atm.bank import ATM
from atm.models import Account
from atm.security import generate_salt, hash_pin

TEST_PIN = "1234"
TEST_BALANCE = Decimal("500.00")


def make_account(balance: Decimal = TEST_BALANCE) -> Account:
    """Build an account with a known PIN (``1234``) and balance."""
    salt = generate_salt()
    return Account(
        owner="Test account",
        pin_hash=hash_pin(TEST_PIN, salt),
        salt=salt,
        balance=balance,
    )


def make_atm(balance: Decimal = TEST_BALANCE) -> ATM:
    """Build an ATM session around a fresh test account."""
    return ATM(make_account(balance))
