"""Interactive command-line interface for the ATM simulation."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Callable

from .bank import ATM
from .config import DEFAULT_BALANCE, DEFAULT_PIN, MINI_STATEMENT_SIZE
from .exceptions import (
    AuthenticationError,
    CardBlockedError,
    InsufficientFundsError,
    InvalidAmountError,
)
from .models import Account
from .security import generate_salt, hash_pin

BANNER = """\
==================================================
          WELCOME TO THE PYTHON ATM
=================================================="""

MENU = """
--------------------------------------------------
MAIN MENU
--------------------------------------------------
1. Check balance
2. Deposit money
3. Withdraw money
4. Mini-statement (last 5 transactions)
5. Exit"""

LINE = "-" * 50


class AtmCli:
    """Console front-end; all input and output is injectable for testing."""

    def __init__(
        self,
        atm: ATM,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        self._atm = atm
        self._input = input_fn
        self._output = output_fn

    def run(self) -> None:
        """Run one full ATM session: banner, PIN login, menu loop."""
        self._output(BANNER)
        if not self._login():
            return
        self._menu_loop()

    # -- login ---------------------------------------------------------

    def _login(self) -> bool:
        """Ask for the PIN until it is correct or the card is blocked."""
        while True:
            pin = self._input("Enter your 4-digit PIN: ").strip()
            try:
                self._atm.authenticate(pin)
            except CardBlockedError as exc:
                self._output("Incorrect PIN.")
                self._output(f"\n{exc}")
                self._output("Please contact your bank. Goodbye!")
                return False
            except AuthenticationError as exc:
                self._output(str(exc))
                continue
            self._output("\nLogin successful! Welcome back.")
            return True

    # -- menu loop -----------------------------------------------------

    def _menu_loop(self) -> None:
        while True:
            self._output(MENU)
            choice = self._input("\nChoose an option (1-5): ").strip()
            try:
                if choice == "1":
                    self._check_balance()
                elif choice == "2":
                    self._deposit()
                elif choice == "3":
                    self._withdraw()
                elif choice == "4":
                    self._print_statement()
                elif choice == "5":
                    self._goodbye()
                    return
                else:
                    self._output("Invalid choice. Please pick a number from 1 to 5.")
            except (InvalidAmountError, InsufficientFundsError) as exc:
                self._output(f"Transaction failed: {exc}")

    def _check_balance(self) -> None:
        transaction = self._atm.check_balance()
        self._output(f"\nYour current balance is: ${transaction.balance_after:,.2f}")

    def _deposit(self) -> None:
        transaction = self._atm.deposit(self._read_amount("deposit"))
        self._output(
            f"Deposited ${transaction.amount:,.2f}. "
            f"New balance: ${transaction.balance_after:,.2f}"
        )

    def _withdraw(self) -> None:
        transaction = self._atm.withdraw(self._read_amount("withdraw"))
        self._output(
            f"Withdrew ${transaction.amount:,.2f}. "
            f"New balance: ${transaction.balance_after:,.2f}"
        )

    def _print_statement(self) -> None:
        entries = self._atm.mini_statement()
        if not entries:
            self._output("\nNo transactions yet. Deposit or withdraw some money first!")
            return
        self._output(
            f"\nMINI-STATEMENT (last {MINI_STATEMENT_SIZE} transactions, newest first)"
        )
        self._output(LINE)
        for number, entry in enumerate(entries, start=1):
            self._output(f"  {number}. {entry.describe()}")

    def _goodbye(self) -> None:
        self._output(f"\nFinal balance: ${self._atm.account.balance:,.2f}")
        self._output("Thank you for using the Python ATM. Goodbye!")

    def _read_amount(self, verb: str) -> Decimal:
        raw = self._input(f"Enter amount to {verb}: $").strip()
        try:
            amount = Decimal(raw)
        except InvalidOperation:
            raise InvalidAmountError(f"'{raw}' is not a valid number.") from None
        return amount


def main() -> None:
    """Create the simulated account and start one CLI session."""
    salt = generate_salt()
    account = Account(
        owner="Checking account",
        pin_hash=hash_pin(DEFAULT_PIN, salt),
        salt=salt,
        balance=DEFAULT_BALANCE,
    )
    AtmCli(ATM(account)).run()


if __name__ == "__main__":
    main()
