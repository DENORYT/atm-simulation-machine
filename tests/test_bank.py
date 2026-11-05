"""Tests for the ATM business-logic layer."""

import unittest
from decimal import Decimal

from atm.exceptions import (
    AuthenticationError,
    CardBlockedError,
    InsufficientFundsError,
    InvalidAmountError,
)
from atm.models import TransactionType
from tests.helpers import TEST_BALANCE, TEST_PIN, make_atm


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.atm = make_atm()

    def test_correct_pin_authenticates(self):
        self.atm.authenticate(TEST_PIN)  # must not raise
        self.assertEqual(self.atm.attempts_remaining, self.atm.MAX_PIN_ATTEMPTS)

    def test_wrong_pin_reports_attempts_remaining(self):
        with self.assertRaises(AuthenticationError) as ctx:
            self.atm.authenticate("0000")
        self.assertIn("2 attempt(s) left", str(ctx.exception))
        self.assertEqual(self.atm.attempts_remaining, 2)

    def test_card_blocks_after_three_wrong_pins(self):
        for _ in range(2):
            with self.assertRaises(AuthenticationError):
                self.atm.authenticate("0000")
        with self.assertRaises(CardBlockedError):
            self.atm.authenticate("0000")

    def test_blocked_card_stays_blocked(self):
        for _ in range(2):
            with self.assertRaises(AuthenticationError):
                self.atm.authenticate("0000")
        with self.assertRaises(CardBlockedError):
            self.atm.authenticate("0000")
        with self.assertRaises(CardBlockedError):
            self.atm.authenticate("0000")  # already blocked

    def test_successful_login_resets_the_attempt_counter(self):
        with self.assertRaises(AuthenticationError):
            self.atm.authenticate("0000")
        self.atm.authenticate(TEST_PIN)
        self.assertEqual(self.atm.attempts_remaining, self.atm.MAX_PIN_ATTEMPTS)


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.atm = make_atm()  # balance 500.00

    def test_deposit_increases_balance_and_is_recorded(self):
        txn = self.atm.deposit(Decimal(250))
        self.assertEqual(self.atm.account.balance, Decimal("750.00"))
        self.assertEqual(txn.kind, TransactionType.DEPOSIT)
        self.assertEqual(len(self.atm.account.transactions), 1)

    def test_withdraw_decreases_balance(self):
        txn = self.atm.withdraw(Decimal("120.50"))
        self.assertEqual(self.atm.account.balance, Decimal("379.50"))
        self.assertEqual(txn.kind, TransactionType.WITHDRAWAL)

    def test_withdraw_more_than_balance_is_refused(self):
        with self.assertRaises(InsufficientFundsError):
            self.atm.withdraw(Decimal("500.01"))
        self.assertEqual(self.atm.account.balance, TEST_BALANCE)
        self.assertEqual(self.atm.account.transactions, [])

    def test_withdraw_exact_balance_is_allowed(self):
        self.atm.withdraw(TEST_BALANCE)
        self.assertEqual(self.atm.account.balance, Decimal("0.00"))

    def test_non_positive_amounts_are_rejected(self):
        for bad in (Decimal(0), Decimal(-1), Decimal("-0.01")):
            with self.assertRaises(InvalidAmountError):
                self.atm.deposit(bad)
            with self.assertRaises(InvalidAmountError):
                self.atm.withdraw(bad)

    def test_non_numeric_and_infinite_amounts_are_rejected(self):
        with self.assertRaises(InvalidAmountError):
            self.atm.deposit("100")  # type: ignore[arg-type]
        with self.assertRaises(InvalidAmountError):
            self.atm.deposit(Decimal("Infinity"))

    def test_balance_inquiry_records_a_transaction(self):
        txn = self.atm.check_balance()
        self.assertEqual(txn.kind, TransactionType.BALANCE_INQUIRY)
        self.assertEqual(txn.balance_after, TEST_BALANCE)

    def test_mini_statement_is_newest_first_and_limited(self):
        for amount in ("1", "2", "3", "4", "5", "6", "7"):
            self.atm.deposit(Decimal(amount))
        statement = self.atm.mini_statement()
        self.assertEqual(len(statement), 5)
        self.assertEqual(statement[0].amount, Decimal(7))
        self.assertEqual(statement[-1].amount, Decimal(3))

    def test_describe_formats_deposit(self):
        txn = self.atm.deposit(Decimal(25))
        self.assertIn("Deposit", txn.describe())
        self.assertIn("+$25.00", txn.describe())


if __name__ == "__main__":
    unittest.main()
