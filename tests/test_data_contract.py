"""校验可供分析的资料关系。"""

import unittest

from scripts.inspect_sources import read_table


class SourceContractTest(unittest.TestCase):
    def test_source_observations_and_references(self):
        shifts = {row["shift"]: row for row in read_table("shifts")}
        claims = {row["claim"]:row for row in read_table("work")}
        self.assertTrue(all(row["shift"] in shifts for row in claims.values()))
        self.assertTrue(any(row["scan_end"] is None for row in shifts.values()))
        s1, s2 = shifts["S060"], shifts["S062"]
        self.assertEqual(s1["worker"], s2["worker"])
        self.assertLess(s2["scan_start"], s1["scan_end"])
        versions = [row for row in read_table("inspection") if row["pack"]=="P06"]
        self.assertTrue(any(row["related_claim"] == "C061" and row["bank_state"] == "已到账" for row in read_table("payments")))
        self.assertIn("C061", versions[0]["accepted_claims"])
        self.assertNotIn("C061", versions[1]["accepted_claims"])
        self.assertEqual({row["month"] for row in shifts.values()}, {"2026-01","2026-02"})
