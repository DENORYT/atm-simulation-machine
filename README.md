# ATM Simulation Machine

A simple console-based ATM simulation written in pure Python — no libraries, just
basic control flow. Great as a first Python project for practicing loops,
conditions, and lists.

## What it does

1. Starts with a fixed account balance and a 4-digit PIN.
2. The user must enter the correct PIN (up to **3 tries** — after that the card
   is "blocked").
3. Once logged in, a menu loop lets the user:
   - **Check balance**
   - **Deposit money** (must be a positive number)
   - **Withdraw money** (with checks so they can't withdraw more than they have)
   - **View mini-statement** (the last few transactions, newest first)
   - **Exit** (prints the final balance)

## Concepts used

| Concept | Where it appears |
|---|---|
| `while` loops | PIN retry loop + main menu loop |
| Counter variables | `attempts` counts wrong PIN entries |
| Conditions | `if amount > balance` overdraw check, menu branching |
| List `.append()` | Recording each transaction for the mini-statement |

## How to run

```bash
python atm.py
```

- Default PIN: `1234`
- Starting balance: `$5,000.00`

Change both at the top of `atm.py`:

```python
CORRECT_PIN = "1234"
balance = 5000.00
MAX_PIN_TRIES = 3
```

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
Insufficient funds! Your balance is only $5,000.00.
```
