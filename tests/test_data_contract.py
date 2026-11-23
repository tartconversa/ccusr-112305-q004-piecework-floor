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

    def test_wage_legs_inputs(self):
        sources = [read_table(name) for name in ['site_assignments', 'appeals', 'bank_legs', 'payments']]
        self.assertEqual({x["actual_site"] for x in sources[0] if x["window"]=="N6"},{"甲","乙"})
        self.assertEqual({x["decision"] for x in sources[1]},{"提交","部分确认","重新申报"})
        payments={x["payment"] for x in sources[3]}
        self.assertTrue(all(x["payment"] in payments for x in sources[2]))
        self.assertEqual({x["kind"] for x in sources[2] if x["movement"]=="PAY-01"},
                         {"已扣账待回执","拒付","拒付重复通知"})

