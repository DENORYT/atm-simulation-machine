"""ATM Simulation Machine.

A professional console ATM simulation built in pure Python (zero runtime
dependencies), demonstrating clean project structure: layered business
logic, typed domain models, custom exceptions, PIN hashing, and a full
unit-test suite.
"""

from .bank import ATM
from .config import DEFAULT_BALANCE, DEFAULT_PIN, MAX_PIN_ATTEMPTS, MINI_STATEMENT_SIZE
from .models import Account, Transaction, TransactionType

__version__ = "1.0.0"

__all__ = [
    "ATM",
    "DEFAULT_BALANCE",
    "DEFAULT_PIN",
    "MAX_PIN_ATTEMPTS",
    "MINI_STATEMENT_SIZE",
    "Account",
    "Transaction",
    "TransactionType",
    "__version__",
]
