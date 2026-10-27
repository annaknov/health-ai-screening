# Health AI Screening Tool

[![tests](https://github.com/annaknov/health-ai-screening/actions/workflows/ci.yml/badge.svg)](https://github.com/annaknov/health-ai-screening/actions/workflows/ci.yml)

A screening tool that tells builders of healthcare AI which California and federal laws, voluntary risk frameworks, and documented real-world failures are relevant to their product. It is meant for founders and product teams who need a first-pass view of regulatory exposure before they pay for legal review.

> **Screening tool, not legal advice.** A lawyer should confirm applicability before launch. The knowledge base covers California and federal law only. It does not cover other states, the EU AI Act, contracts, or payer policies.

## What it does

You describe your tool and answer a 21-question intake (organization type, what the tool does, model type, data, outputs, human oversight, reach). Each answer sets a **tag** (`phi`, `genai`, `clinician_review`, and so on). Every row in the knowledge base carries a `trigger_rule`, a Boolean expression over those tags. The matcher evaluates every rule against your profile and sorts each row into:

- **Applies**: the rule is true however your "unsure" answers resolve.
- **Depends**: the rule is true only for some values of your unsure answers, and the output names which ones.
- **Not applicable**: the rule is false either way.

Unsure answers are evaluated both ways, so a "not sure" never silently turns a law off.

| Knowledge base file | Rows | What it holds |
|---|---|---|
| `california-laws.csv` | 31 | California statutes, regulations, AG guidance, and bills (including vetoed and died) |
| `federal-laws.csv` | 41 | Federal statutes, rules, guidance, executive orders, and proposed rules |
| `risks-best-practices.csv` | 67 | Risks and recommended practices from NIST, CHAI, Joint Commission/CHAI, FDA guiding principles, and WHO |
| `ai-failure-examples.csv` | 30 | Documented AI and algorithmic failures (20 health, 10 outside health), each linked to the risks it illustrates |

Rows carry their status (enacted, final, proposed, vetoed, and so on), effective dates, a verification level, and a primary source link. Only `enacted` and `final` rows are obligations; the rest are signals. Risks and best practices are voluntary frameworks, not law. See [docs/data-dictionary.md](docs/data-dictionary.md) for every column.

**Data currency.** Laws were last built 2026-10-06, risks 2026-10-07 (four rows 2026-10-15), and failure examples 2026-10-12 (see each row's `as_of`). Check anything after those dates against primary sources.

## Two ways to use it

### Option A: As a Claude Project (guided intake and designed report)

This is the intended experience: Claude runs the questionnaire, calls the matcher, and publishes an HTML report.

1. Create a new Project in Claude.
2. Paste [`prompts/project-instructions.md`](prompts/project-instructions.md) (everything below the divider line) into the Project's instructions.
3. Upload these files to the Project knowledge:
   - `knowledge_base/intake-questionnaire.md`
   - `knowledge_base/tag-schema.md`
   - `knowledge_base/match_tool.py`
   - `knowledge_base/california-laws.csv`, `federal-laws.csv`, `risks-best-practices.csv`, `ai-failure-examples.csv`
   - `templates/report-example.html` (the approved report template)
   - `knowledge_base/imdrf-gmlp-guiding-principles-summary.md` (optional, enables the IMDRF follow-up)
4. Open a chat in the Project and type `Start`.

Claude asks the questions, runs `match_tool.py`, and produces a report with: summary, laws in detail, risks with proposed edits, matched real-world cases, laws considered and ruled out, and the assumptions it made. Follow-up questions are answered in chat.

### Option B: As a command-line matcher (no AI, no dependencies)

Python 3.9+ and the standard library only.

```bash
git clone https://github.com/annaknov/health-ai-screening.git
cd health-ai-screening

# Inline tags: yes, unsure; anything omitted is "no"
python knowledge_base/match_tool.py --tags 'genai=yes,chatbot=yes,phi=yes,ca_users=yes,clinician_review=unsure'

# Or from a JSON profile
python knowledge_base/match_tool.py --profile examples/example-profile.json

# Machine-readable output, and include rows that don't apply
python knowledge_base/match_tool.py --profile examples/example-profile.json --json
python knowledge_base/match_tool.py --profile examples/example-profile.json --not-applicable
```

Example output (abridged):

```
## APPLIES (69)
  laws:
    CA-CIPA-632  California Invasion of Privacy Act ...  (enacted, effective 1967-11-08)
    US-1557-2024  ACA Section 1557 Nondiscrimination Final Rule (2024)  (final, effective 2024-07-05)
    ...
  risks:
    R-LABEL-PROXY-BIAS  Cost or utilization used as a stand-in for health need  (high priority)
```

To build a profile, read [`knowledge_base/intake-questionnaire.md`](knowledge_base/intake-questionnaire.md): each answer lists the tags it sets (`tag` = yes, `tag?` = unsure). Valid tags are listed in [`knowledge_base/tag-schema.md`](knowledge_base/tag-schema.md). Derived tags (`hipaa_entity`, `hhs_funded`, `ccpa_business`, `possible_device`, and others) are computed automatically; do not set them yourself.

| Flag | Purpose |
|---|---|
| `--tags 'a=yes,b=unsure'` | Inline profile |
| `--profile FILE.json` | Profile as `{"tag": "yes" \| "unsure"}` |
| `--dir FOLDER` | Read the CSVs from another folder (default: next to the script) |
| `--not-applicable` | Also list rows that don't apply |
| `--diff FOLDER` | Show rows whose result changes between two knowledge-base versions |
| `--json` | JSON output |

`--profile-name` loads a named profile from `evals/tag_profiles.json`, which is not included in this repository.

## Interpreting results

The matcher screens for **scope**. It does not capture every exemption or threshold. Before relying on a matched law, read that row's `exclusions`, `key_definitions`, and `key_questions` in the CSV, and check `status`, `effective_date`, `effective_date_notes`, and `verification_level`. Treat `unverified` and `partially_verified` rows with extra caution. FDA device classifications should be read as "depends on intended use," not as a determination that a tool is or isn't a device.

## Repository layout

```
knowledge_base/       Data and logic: CSVs, tag schema, questionnaire, match_tool.py
prompts/              Claude Project instructions
templates/            Approved HTML report template
examples/             Sample tag profile
tests/                Data-integrity and logic tests
docs/                 Data dictionary
.github/workflows/    CI
```

## Development

```bash
python -m unittest discover -s tests -v
```

The tests check that every `trigger_rule` parses, every tag used in a rule exists in `tag-schema.md`, IDs are unique, cross-references between files resolve, and the three-valued logic behaves as documented. Run them after any edit to a CSV or the schema. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Optional IMDRF framework

`knowledge_base/imdrf-gmlp-guiding-principles-summary.md` is a short paraphrase of the ten IMDRF *Good machine learning practice* principles (IMDRF/AIML WG/N88, 2025). Upload it to your Claude Project to enable the "draw on IMDRF" option in the follow-up menu. The IMDRF PDF itself is copyrighted and is not redistributed here; download it from [imdrf.org](https://www.imdrf.org).

## License

Code and original text are released under the [MIT License](LICENSE). The knowledge base summarizes and links to third-party laws, regulations, and published frameworks; those sources remain the property of their publishers and are cited by URL in each row.
