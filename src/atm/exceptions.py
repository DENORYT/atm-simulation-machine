"""Custom exception hierarchy for the ATM simulation."""


class ATMError(Exception):
    """Base class for all ATM simulation errors."""


class InvalidAmountError(ATMError):
    """Raised when a deposit or withdrawal amount is not valid."""


class InsufficientFundsError(ATMError):
    """Raised when a withdrawal exceeds the available balance."""


class AuthenticationError(ATMError):
    """Raised when PIN authentication fails."""


class CardBlockedError(AuthenticationError):
    """Raised when the card is blocked after too many failed attempts."""
