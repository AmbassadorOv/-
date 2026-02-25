#!/usr/bin/env python3
import unittest
import json
import os
import Kernel.validator as validator
import Gatekeeper.rov_signal as rov_signal
import jules_core

class TestDiamondLogic(unittest.TestCase):
    def test_digital_root(self):
        self.assertEqual(validator.digital_root(441), 9)
        self.assertEqual(validator.digital_root(10), 1)
        self.assertEqual(validator.digital_root(1), 1)
        self.assertEqual(validator.digital_root(9), 9)

    def test_validate_logic(self):
        # 441 should be valid (root 9)
        self.assertTrue(validator.validate_logic(441))
        # 10 should be valid (root 1)
        self.assertTrue(validator.validate_logic(10))
        # "A" is ASCII 65 -> 6+5=11 -> 1+1=2 (Invalid)
        self.assertFalse(validator.validate_logic("A"))

        # Payload string test
        # "6" -> ASCII 54 -> 5+4=9 (Valid)
        self.assertTrue(validator.validate_logic("6"))

    def test_signal_sanitization(self):
        toxic = "I hope this magic certainly works, of course!"
        sanitized = rov_signal.gatekeep(toxic)
        self.assertNotIn("hope", sanitized.lower())
        self.assertNotIn("magic", sanitized.lower())
        self.assertIn("[SIGNAL_PURGED]", sanitized)

    def test_agent_recruitment(self):
        # Recruitment should register agents in the DB
        group = "Group Arich"
        aid = jules_core.convert_to_agent(group)
        self.assertIsNotNone(aid)

        import sqlite3
        conn = sqlite3.connect("julius_master.db")
        c = conn.cursor()
        c.execute("SELECT name FROM agents WHERE id = ?", (aid,))
        row = c.fetchone()
        conn.close()
        self.assertEqual(row[0], group)

    def test_231_gates(self):
        brain = jules_core.build_dense_core(231)
        self.assertEqual(len(brain.gates), 231)
        self.assertIn("Aleph-Bet", brain.gates)
        self.assertIn("Shin-Tav", brain.gates)

if __name__ == "__main__":
    unittest.main()
