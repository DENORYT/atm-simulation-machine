"""Default configuration values for the ATM simulation.

These constants emulate the data a real ATM would receive from a secure
banking backend. Adjust them to change the simulated account.
"""

from decimal import Decimal

#: The fixed 4-digit PIN of the simulated account.
DEFAULT_PIN = "1234"

#: Starting account balance.
DEFAULT_BALANCE = Decimal("5000.00")

#: Number of PIN attempts allowed before the card is blocked.
MAX_PIN_ATTEMPTS = 3

#: Number of transactions shown in the mini-statement.
MINI_STATEMENT_SIZE = 5
