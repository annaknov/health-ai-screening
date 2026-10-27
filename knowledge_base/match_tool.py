#!/usr/bin/env python3
"""Match one tool's tag profile against the law and risk CSVs. Standalone: also shipped in the upload package.

Loads california-laws.csv, federal-laws.csv, and risks-best-practices.csv from --dir (default: this file's
folder), computes the derived tags from intake-questionnaire.md, evaluates every trigger_rule with each unsure
tag tried both ways, and prints Applies / Depends / Not applicable with status and effective date (laws) or
priority (risks). Status filtering for the report is left to the reader: the status is printed on every law.

Usage:
  match_tool.py --tags 'genai=yes,chatbot=yes,clinician_review=unsure'
  match_tool.py --profile profile.json            ({"tag": "yes" | "unsure"}; absent tags are "no")
  match_tool.py --profile-name SCR                (from evals/tag_profiles.json, repo only)
  options: --dir <folder>  --not-applicable  --diff <other folder> (compare two builds)  --json
"""
import argparse
import csv
import itertools
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
FILES = ["california-laws.csv", "federal-laws.csv", "risks-best-practices.csv"]
OPTIONAL_FILES = ["ai-failure-examples.csv"]  # loaded when present
TOKEN = re.compile(r"\(|\)|AND|OR|NOT|ALWAYS|[a-z0-9_]+")


def evaluate(rule, profile):
    """Three-valued rule evaluation. Returns ('applies' | 'possibly' | None, [unsure tags it hinges on])."""
    rule = rule.strip()
    if rule == "ALWAYS":
        return "applies", []
    if "".join(TOKEN.findall(rule)) != re.sub(r"\s+", "", rule):
        raise ValueError(f"bad rule: {rule}")
    names = sorted(set(re.findall(r"\b[a-z0-9_]+\b", rule)))
    unsure = [n for n in names if profile.get(n) == "unsure"]
    expr = re.sub(r"\bAND\b", " and ", re.sub(r"\bOR\b", " or ", re.sub(r"\bNOT\b", " not ", rule)))
    results = []
    for combo in itertools.product([True, False], repeat=len(unsure)):
        env = {n: profile.get(n) == "yes" for n in names}
        env.update(dict(zip(unsure, combo)))
        results.append(eval(expr, {"__builtins__": {}}, env))
    if all(results):
        return "applies", []
    if any(results):
        return "possibly", unsure
    return None, []


# Derived tags (intake-questionnaire.md v0.8): (rule that makes it yes, rule that makes it at least unsure).
# Computed in order; an explicit "yes" from the intake is never lowered.
DERIVED = [
    ("patient_facing", "patient_facing OR patient_comm", None),
    ("health_info", "phi OR consumer_health_data OR substance_use_records OR neural_data", None),
    ("non_hipaa_personal_info", "consumer_health_data OR neural_data OR other_personal_info", None),
    ("hipaa_entity", "phi", "org_provider OR org_plan"),
    ("hhs_funded", "plan_medicare_advantage OR plan_medicaid_chip OR plan_marketplace", "org_provider OR org_developer"),
    ("ccpa_business", "ca_users AND NOT org_government AND (revenue_over_ccpa OR data_seller OR (ca_100k AND shares_personal_data))", None),
    ("large_genai_platform", "genai AND generates_media AND large_scale", None),
    ("possible_device", "(cdss AND (fda_pathway OR analyzes_images_signals OR patient_facing OR time_critical"
                        " OR basis_not_reviewable)) OR digital_therapeutic OR fda_pathway", None),
    ("minors_possible", "minors_possible OR under_13_possible", None),
]


def add_derived(profile):
    prof = dict(profile)
    for tag, yes_rule, unsure_rule in DERIVED:
        if prof.get(tag) == "yes":
            continue
        res, _ = evaluate(yes_rule, prof)
        if res == "applies":
            prof[tag] = "yes"
        elif res == "possibly" or (unsure_rule and evaluate(unsure_rule, prof)[0]):
            prof[tag] = "unsure"
    return prof


def load(folder):
    rows = []
    names = FILES + [n for n in OPTIONAL_FILES if os.path.exists(os.path.join(folder, n))]
    for name in names:
        with open(os.path.join(folder, name), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rid = r.get("law_id") or r.get("risk_id") or r.get("example_id")
                if "law_id" in r:
                    info = f"{r['status']}, effective {r['effective_date'] or 'n/a'}"
                elif "example_id" in r:
                    info = f"{r['domain']}, {r['evidence_status']}; illustrates {r['related_risk_ids']}"
                else:
                    info = f"{r['priority']} priority"
                rows.append((rid, r.get("title", ""), r["trigger_rule"], info))
    return rows


def match(rows, profile):
    out = {rid: (title, info) + evaluate(rule, profile) for rid, title, rule, info in rows}
    # An example is shown only if its own rule matches AND at least one risk it illustrates matches.
    for rid, (title, info, res, hinge) in list(out.items()):
        if rid.startswith("EX-") and res:
            linked = [x.strip() for x in info.split("illustrates ", 1)[1].split(";") if x.strip()]
            if not any(out.get(x, (None, None, None))[2] for x in linked):
                out[rid] = (title, info, None, [])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=HERE)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--profile")
    g.add_argument("--profile-name")
    g.add_argument("--tags")
    ap.add_argument("--not-applicable", action="store_true")
    ap.add_argument("--diff")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.profile:
        profile = json.load(open(a.profile))
    elif a.profile_name:
        profile = json.load(open(os.path.join(ROOT, "evals/tag_profiles.json")))[a.profile_name]
    else:
        profile = dict(kv.strip().split("=") for kv in a.tags.split(","))
    profile = add_derived(profile)
    cur = match(load(a.dir), profile)
    if a.diff:
        old = match(load(a.diff), profile)
        for rid in sorted(set(cur) | set(old)):
            o = old.get(rid, (None, None, "absent"))[2] or "not"
            c = cur.get(rid, (None, None, "absent"))[2] or "not"
            if o != c:
                print(f"{rid}: {o} -> {c}")
        return
    if a.json:
        print(json.dumps({"profile": profile, "results": {
            rid: {"title": t, "info": i, "result": r or "not", "depends_on": h} for rid, (t, i, r, h) in cur.items()}}, indent=1))
        return
    labels = {"applies": "APPLIES", "possibly": "DEPENDS", None: "NOT APPLICABLE"}
    for res in ("applies", "possibly", None):
        if res is None and not a.not_applicable:
            continue
        items = [(rid, v) for rid, v in cur.items() if v[2] == res]
        print(f"\n## {labels[res]} ({len(items)})")
        for name, prefixes in (("laws", ("CA-", "US-")), ("risks", ("R-", "P-")), ("examples", ("EX-",))):
            sel = [(rid, v) for rid, v in items if rid.startswith(prefixes)]
            if sel:
                print(f"  {name}:")
            for rid, (title, info, _, hinge) in sel:
                extra = f"  [depends on: {', '.join(hinge)}]" if hinge else ""
                print(f"    {rid}  {title}  ({info}){extra}")


if __name__ == "__main__":
    main()
