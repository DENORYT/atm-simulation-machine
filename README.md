# ATM Simulation Machine

[![CI](https://github.com/DENORYT/atm-simulation-machine/actions/workflows/ci.yml/badge.svg)](https://github.com/DENORYT/atm-simulation-machine/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/lint-ruff-261230)](https://docs.astral.sh/ruff/)

A professional, console-based **ATM simulation** written in pure Python — zero
runtime dependencies. It emulates the core flow of a real ATM: secure PIN login
with limited attempts, balance inquiries, deposits, overdraft-protected
withdrawals, and a mini-statement of recent transactions.

## Features

- **PIN authentication** — up to 3 attempts, then the card is "blocked";
  PINs are stored as salted SHA-256 hashes and compared in constant time
- **Check balance** — every inquiry is recorded as a transaction
- **Deposit money** — strictly positive amounts, exact `Decimal` money math
- **Withdraw money** — refuses overdrafts and invalid amounts
- **Mini-statement** — the last 5 transactions, newest first, with timestamps
- **Clean architecture** — business logic fully separated from the console UI
  (all I/O is injectable), which makes every layer unit-testable

## Quick start

Requires Python 3.9+.

```bash
git clone https://github.com/DENORYT/atm-simulation-machine.git
cd atm-simulation-machine
pip install -e .

atm            # via the installed console script
# or
python -m atm  # without installing
```

Default credentials for the simulation: **PIN `1234`**, balance **$5,000.00**.

## Example session

```text
==================================================
          WELCOME TO THE PYTHON ATM
==================================================

Enter your 4-digit PIN: 9999
Incorrect PIN. 2 attempt(s) left.

Enter your 4-digit PIN: 1234

Login successful! Welcome back.

--------------------------------------------------
MAIN MENU
--------------------------------------------------
1. Check balance
2. Deposit money
3. Withdraw money
4. Mini-statement (last 5 transactions)
5. Exit

Choose an option (1-5): 3
Enter amount to withdraw: $99999
Transaction failed: Insufficient funds! Available balance is $5,000.00.

Choose an option (1-5): 4

MINI-STATEMENT (last 5 transactions, newest first)
--------------------------------------------------
  1. 2026-11-05 19:52 | Deposit          | +$250.00
  2. 2026-11-05 19:51 | Balance inquiry  |  $5,000.00
```

## Project structure

```text
atm-simulation-machine/
├── src/atm/
│   ├── __init__.py        # Public API and version
│   ├── __main__.py        # python -m atm entry point
│   ├── app.py             # CLI layer: menus, prompts, output
│   ├── bank.py            # Business logic: auth, deposits, withdrawals
│   ├── config.py          # Defaults (PIN, balance, limits)
│   ├── exceptions.py      # Custom exception hierarchy
│   ├── models.py          # Account, Transaction, TransactionType
│   └── security.py        # Salted PIN hashing (SHA-256 + hmac)
├── tests/                 # Unit + end-to-end CLI tests (stdlib unittest)
├── .github/workflows/     # CI: tests on Python 3.9–3.13 + ruff lint
├── pyproject.toml         # Packaging metadata and tool config
└── LICENSE                # MIT
```

### Architecture

| Layer | Module | Responsibility |
|---|---|---|
| UI | `app.py` | Prompts, menus, formatting — no business rules |
| Domain logic | `bank.py` | Authentication state machine, transaction rules |
| Models | `models.py` | Immutable `Transaction` records, mutable `Account` |
| Security | `security.py` | Salted hashing, constant-time verification |
| Errors | `exceptions.py` | Typed errors the UI maps to friendly messages |

Money is handled with [`Decimal`](https://docs.python.org/3/library/decimal.html)
(never floats) and quantized to 2 decimal places.

## Configuration

Change the simulated account by editing `src/atm/config.py` or passing your own
`Account` to `ATM` programmatically:

```python
from decimal import Decimal
from atm import ATM
from atm.models import Account
from atm.security import generate_salt, hash_pin

salt = generate_salt()
account = Account(
    owner="Savings",
    pin_hash=hash_pin("9999", salt),
    salt=salt,
    balance=Decimal("10000.00"),
)
AtmCli(ATM(account)).run()
```

## Testing

The test suite (34 tests) covers PIN hashing, the authentication state machine,
transaction rules, and full scripted CLI sessions:

```bash
python -m unittest discover -v
```

CI runs the suite on Python 3.9–3.13 plus a ruff lint job on every push and
pull request.

## Concepts demonstrated

| Concept | Where |
|---|---|
| `while` loops | PIN retry loop and main menu loop (`app.py`) |
| Counter variables | Failed-PIN counting in `bank.py` |
| Conditions | Overdraw check, menu branching, input validation |
| List `.append()` | Recording transactions for the mini-statement |
| Dataclasses & enums | `models.py` |
| Custom exceptions | `exceptions.py` |
| `Decimal` money math | `bank.py`, `config.py` |

## License

[MIT](LICENSE) © 2026 DENORYT
