"""End-to-end CLI tests using scripted input and captured output."""

import unittest

from atm.app import AtmCli
from tests.helpers import TEST_PIN, make_atm


class AtmCliSessionTests(unittest.TestCase):
    def run_session(self, script):
        """Run a CLI session with scripted keystrokes; return the transcript."""
        outputs = []
        inputs = iter(script)
        cli = AtmCli(
            make_atm(),
            input_fn=lambda prompt="": next(inputs),
            output_fn=outputs.append,
        )
        cli.run()
        return "\n".join(outputs)

    def test_full_session(self):
        transcript = self.run_session(
            ["9999", "0000", TEST_PIN, "1", "2", "250", "3", "120.50", "4", "5"]
        )
        self.assertIn("Login successful", transcript)
        self.assertIn("$500.00", transcript)
        self.assertIn("Deposited $250.00", transcript)
        self.assertIn("Withdrew $120.50", transcript)
        self.assertIn("MINI-STATEMENT", transcript)
        self.assertIn("Final balance: $629.50", transcript)
        self.assertIn("Goodbye!", transcript)

    def test_overdraft_is_refused(self):
        transcript = self.run_session([TEST_PIN, "3", "99999", "5"])
        self.assertIn("Insufficient funds! Available balance is $500.00", transcript)
        self.assertIn("Final balance: $500.00", transcript)

    def test_non_numeric_amount_is_refused(self):
        transcript = self.run_session([TEST_PIN, "2", "abc", "5"])
        self.assertIn("not a valid number", transcript)

    def test_invalid_menu_choice_is_reported(self):
        transcript = self.run_session([TEST_PIN, "9", "5"])
        self.assertIn("Invalid choice", transcript)

    def test_empty_statement_message(self):
        transcript = self.run_session([TEST_PIN, "4", "5"])
        self.assertIn("No transactions yet", transcript)

    def test_card_blocks_after_three_wrong_pins(self):
        transcript = self.run_session(["1111", "2222", "3333"])
        self.assertIn("card is blocked", transcript.lower())
        self.assertNotIn("Login successful", transcript)


if __name__ == "__main__":
    unittest.main()
