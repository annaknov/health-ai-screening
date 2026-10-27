"""Data-integrity and logic tests. Run from the repo root:  python -m unittest discover -s tests -v"""
import csv
import json
import os
import re
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KB = os.path.join(ROOT, "knowledge_base")
sys.path.insert(0, KB)
import match_tool as mt  # noqa: E402

CSVS = ["california-laws.csv", "federal-laws.csv", "risks-best-practices.csv", "ai-failure-examples.csv"]


def rows(name):
    with open(os.path.join(KB, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def schema_tags():
    """Every backticked tag in the first column of tag-schema.md tables."""
    with open(os.path.join(KB, "tag-schema.md"), encoding="utf-8") as fh:
        text = fh.read()
    text = text.split("## Changes from")[0]
    return set(re.findall(r"^\| `([a-z0-9_]+)` \|", text, flags=re.M))


def rule_tags(rule):
    return set(re.findall(r"\b[a-z0-9_]+\b", rule))


class RuleSyntax(unittest.TestCase):
    def test_all_rules_parse_and_use_known_tags(self):
        known = schema_tags()
        self.assertGreater(len(known), 50)
        for name in CSVS:
            for r in rows(name):
                rid = r.get("law_id") or r.get("risk_id") or r.get("example_id")
                rule = r["trigger_rule"]
                mt.evaluate(rule, {})  # raises ValueError on a malformed rule
                if rule.strip() != "ALWAYS":
                    unknown = rule_tags(rule) - known
                    self.assertFalse(unknown, f"{rid} uses tags not in tag-schema.md: {sorted(unknown)}")

    def test_derived_rules_use_known_tags(self):
        known = schema_tags()
        for tag, yes_rule, unsure_rule in mt.DERIVED:
            self.assertIn(tag, known)
            for rule in (yes_rule, unsure_rule):
                if rule:
                    self.assertFalse(rule_tags(rule) - known, f"derived rule for {tag}")


class DataIntegrity(unittest.TestCase):
    def test_ids_unique_and_present(self):
        ids = []
        for name in CSVS:
            for r in rows(name):
                rid = r.get("law_id") or r.get("risk_id") or r.get("example_id")
                self.assertTrue(rid, f"empty id in {name}")
                ids.append(rid)
        self.assertEqual(len(ids), len(set(ids)), "duplicate ids across CSVs")

    def test_cross_references_resolve(self):
        ids = {(r.get("law_id") or r.get("risk_id") or r.get("example_id"))
               for n in CSVS for r in rows(n)}
        for r in rows("ai-failure-examples.csv"):
            for x in filter(None, (s.strip() for s in r["related_risk_ids"].split(";"))):
                self.assertIn(x, ids, f"{r['example_id']} -> {x}")
        for r in rows("risks-best-practices.csv"):
            for x in filter(None, (s.strip() for s in r["related_law_ids"].split(";"))):
                self.assertIn(x, ids, f"{r['risk_id']} -> {x}")

    def test_law_rows_have_valid_status_and_source(self):
        ok = {"enacted", "final", "proposed", "draft_guidance", "died", "vetoed", "withdrawn", "rescinded", "vacated"}
        for name in ("california-laws.csv", "federal-laws.csv"):
            for r in rows(name):
                self.assertIn(r["status"], ok, r["law_id"])
                self.assertTrue(r["primary_source_url"].startswith("http"), r["law_id"])


class Logic(unittest.TestCase):
    def test_three_valued_rules(self):
        self.assertEqual(mt.evaluate("ALWAYS", {})[0], "applies")
        self.assertEqual(mt.evaluate("a AND b", {"a": "yes", "b": "yes"})[0], "applies")
        self.assertIsNone(mt.evaluate("a AND b", {"a": "yes"})[0])
        res, hinge = mt.evaluate("a AND NOT b", {"a": "yes", "b": "unsure"})
        self.assertEqual((res, hinge), ("possibly", ["b"]))
        self.assertEqual(mt.evaluate("a OR b", {"a": "yes", "b": "unsure"})[0], "applies")

    def test_malformed_rule_rejected(self):
        with self.assertRaises(ValueError):
            mt.evaluate("a AND __import__('os')", {})

    def test_derived_tags(self):
        p = mt.add_derived({"phi": "yes", "plan_marketplace": "yes", "patient_comm": "yes"})
        self.assertEqual(p["hipaa_entity"], "yes")
        self.assertEqual(p["hhs_funded"], "yes")
        self.assertEqual(p["patient_facing"], "yes")
        self.assertEqual(mt.add_derived({"org_developer": "yes"})["hhs_funded"], "unsure")

    def test_example_profile_runs(self):
        with open(os.path.join(ROOT, "examples", "example-profile.json"), encoding="utf-8") as fh:
            profile = json.load(fh)
        out = mt.match(mt.load(KB), mt.add_derived(profile))
        applies = {k for k, v in out.items() if v[2] == "applies"}
        self.assertIn("US-1557-2024", applies)
        self.assertIn("R-LABEL-PROXY-BIAS", applies)


if __name__ == "__main__":
    unittest.main()
