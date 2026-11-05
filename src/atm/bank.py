"""Business logic layer: authentication and transaction handling."""

from __future__ import annotations

from decimal import Decimal

from .config import MAX_PIN_ATTEMPTS, MINI_STATEMENT_SIZE
from .exceptions import (
    AuthenticationError,
    CardBlockedError,
    InsufficientFundsError,
    InvalidAmountError,
)
from .models import Account, Transaction, TransactionType
from .security import verify_pin

_TWO_PLACES = Decimal("0.01")


class ATM:
    """Business logic for a single ATM session operating on one account."""

    MAX_PIN_ATTEMPTS = MAX_PIN_ATTEMPTS

    def __init__(self, account: Account) -> None:
        self._account = account
        self._failed_attempts = 0

    @property
    def account(self) -> Account:
        """The account this ATM session operates on."""
        return self._account

    @property
    def attempts_remaining(self) -> int:
        """How many PIN attempts are left before the card is blocked."""
        return self.MAX_PIN_ATTEMPTS - self._failed_attempts

    # -- authentication ------------------------------------------------

    def authenticate(self, pin: str) -> None:
        """Verify ``pin`` against the account's hashed PIN.

        Raises:
            CardBlockedError: if the card is (or becomes) blocked.
            AuthenticationError: if the PIN is wrong but attempts remain.
        """
        if self._failed_attempts >= self.MAX_PIN_ATTEMPTS:
            raise CardBlockedError("The card is blocked. Please contact your bank.")
        if verify_pin(pin, self._account.salt, self._account.pin_hash):
            self._failed_attempts = 0
            return
        self._failed_attempts += 1
        remaining = self.MAX_PIN_ATTEMPTS - self._failed_attempts
        if remaining <= 0:
            raise CardBlockedError("Too many incorrect attempts. The card is blocked.")
        raise AuthenticationError(f"Incorrect PIN. {remaining} attempt(s) left.")

    # -- transactions --------------------------------------------------

    def deposit(self, amount: Decimal) -> Transaction:
        """Add ``amount`` to the balance and record the transaction."""
        self._validate_amount(amount)
        return self._record(
            TransactionType.DEPOSIT, amount, self._account.balance + amount
        )

    def withdraw(self, amount: Decimal) -> Transaction:
        """Subtract ``amount`` from the balance, refusing overdrafts."""
        self._validate_amount(amount)
        if amount > self._account.balance:
            raise InsufficientFundsError(
                f"Insufficient funds! Available balance is ${self._account.balance:,.2f}."
            )
        return self._record(
            TransactionType.WITHDRAWAL, amount, self._account.balance - amount
        )

    def check_balance(self) -> Transaction:
        """Record a balance inquiry and return it."""
        return self._record(
            TransactionType.BALANCE_INQUIRY, Decimal(0), self._account.balance
        )

    def mini_statement(self, count: int = MINI_STATEMENT_SIZE) -> list[Transaction]:
        """Return the last ``count`` transactions, newest first."""
        return list(reversed(self._account.transactions[-count:]))

    # -- internals -----------------------------------------------------

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if not isinstance(amount, Decimal):
            raise InvalidAmountError("Amount must be a number.")
        if not amount.is_finite():
            raise InvalidAmountError("Amount must be a finite number.")
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than zero.")

    def _record(
        self, kind: TransactionType, amount: Decimal, new_balance: Decimal
    ) -> Transaction:
        self._account.balance = new_balance.quantize(_TWO_PLACES)
        transaction = Transaction(
            kind=kind, amount=amount, balance_after=self._account.balance
        )
        self._account.transactions.append(transaction)
        return transaction
