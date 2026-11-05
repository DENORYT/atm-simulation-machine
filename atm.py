# ============================================================
#  ATM Simulation Machine
# ------------------------------------------------------------
#  A simple console ATM that demonstrates:
#    * while loops        -> PIN retry loop + main menu loop
#    * counter variables  -> counting wrong PIN attempts
#    * conditions         -> overdraw check, menu branching
#    * list .append()     -> building the mini-statement
# ============================================================

# ---------------- Account setup (change these) ----------------
CORRECT_PIN = "1234"      # the fixed 4-digit PIN
balance = 5000.00         # starting account balance
MAX_PIN_TRIES = 3         # how many PIN attempts are allowed

transactions = []         # mini-statement: list of transaction records

print("=" * 50)
print("           WELCOME TO THE PYTHON ATM")
print("=" * 50)

# ---------------- PIN login: up to 3 tries ----------------
attempts = 0              # counter variable
authenticated = False

while attempts < MAX_PIN_TRIES:
    pin = input("\nEnter your 4-digit PIN: ").strip()

    if pin == CORRECT_PIN:
        authenticated = True
        print("\nLogin successful! Welcome back.")
        break

    attempts += 1
    remaining = MAX_PIN_TRIES - attempts
    if remaining > 0:
        print(f"Incorrect PIN. {remaining} attempt(s) left.")
    else:
        print("Incorrect PIN.")

if not authenticated:
    print("\nCard blocked after too many incorrect attempts.")
    print("Please contact your bank. Goodbye!")
else:
    # ---------------- Main menu loop ----------------
    while True:
        print("\n" + "-" * 50)
        print("MAIN MENU")
        print("-" * 50)
        print("1. Check balance")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Mini-statement (last 5 transactions)")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        # ---- 1. Check balance ----
        if choice == "1":
            print(f"\nYour current balance is: ${balance:,.2f}")
            transactions.append(f"Balance inquiry   |  ${balance:,.2f}")

        # ---- 2. Deposit money ----
        elif choice == "2":
            try:
                amount = float(input("Enter amount to deposit: $"))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue

            if amount <= 0:
                print("Deposit amount must be greater than zero.")
            else:
                balance = round(balance + amount, 2)
                print(f"Deposited ${amount:,.2f}. New balance: ${balance:,.2f}")
                transactions.append(f"Deposit           | +${amount:,.2f}")

        # ---- 3. Withdraw money ----
        elif choice == "3":
            try:
                amount = float(input("Enter amount to withdraw: $"))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue

            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
            elif amount > balance:   # can't withdraw more than you have
                print(f"Insufficient funds! Your balance is only ${balance:,.2f}.")
            else:
                balance = round(balance - amount, 2)
                print(f"Withdrew ${amount:,.2f}. New balance: ${balance:,.2f}")
                transactions.append(f"Withdrawal        | -${amount:,.2f}")

        # ---- 4. Mini-statement ----
        elif choice == "4":
            if not transactions:
                print("\nNo transactions yet. Deposit or withdraw some money first!")
            else:
                print("\nMINI-STATEMENT (last 5 transactions, newest first)")
                print("-" * 50)
                recent = list(reversed(transactions[-5:]))
                for i, record in enumerate(recent, start=1):
                    print(f"  {i}. {record}")

        # ---- 5. Exit ----
        elif choice == "5":
            print(f"\nFinal balance: ${balance:,.2f}")
            print("Thank you for using the Python ATM. Goodbye!")
            break

        # ---- Anything else ----
        else:
            print("Invalid choice. Please pick a number from 1 to 5.")
