"""Core domain models: accounts and transactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from .config import DEFAULT_BALANCE


class TransactionType(Enum):
    """Kinds of transactions the ATM can record."""

    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    BALANCE_INQUIRY = "Balance inquiry"

    @property
    def sign(self) -> str:
        """Sign used when rendering the transaction amount in a statement."""
        if self is TransactionType.DEPOSIT:
            return "+"
        if self is TransactionType.WITHDRAWAL:
            return "-"
        return " "


@dataclass(frozen=True)
class Transaction:
    """A single immutable ATM transaction record."""

    kind: TransactionType
    amount: Decimal
    balance_after: Decimal
    timestamp: datetime = field(default_factory=datetime.now)

    def describe(self) -> str:
        """Return a human-readable one-line description for statements."""
        stamp = self.timestamp.strftime("%Y-%m-%d %H:%M")
        if self.kind is TransactionType.BALANCE_INQUIRY:
            change = f" ${self.balance_after:,.2f}"
        else:
            change = f"{self.kind.sign}${self.amount:,.2f}"
        return f"{stamp} | {self.kind.value:<16} | {change}"


@dataclass
class Account:
    """A bank account served by the simulated ATM."""

    owner: str
    pin_hash: str
    salt: str
    balance: Decimal = DEFAULT_BALANCE
    transactions: list[Transaction] = field(default_factory=list)
