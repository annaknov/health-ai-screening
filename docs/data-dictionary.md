# Data dictionary

All files are UTF-8 CSV in `knowledge_base/`. List-valued columns use `; ` as the separator.

## Shared by every file

| Column | Meaning |
|---|---|
| `trigger_rule` | Boolean expression over tags: `AND`, `OR`, `NOT`, parentheses, or `ALWAYS`. Tags are defined in `tag-schema.md`. |
| `as_of` | Date the row was built. Developments after this date may not be reflected. |

## `california-laws.csv` and `federal-laws.csv`

| Column | Meaning |
|---|---|
| `law_id` | Stable ID (`CA-...` or `US-...`). Internal; not shown in reports. |
| `jurisdiction` | `California` or `Federal`. |
| `instrument_type` | `statute`, `regulation`, `bill`, `guidance`, `program`, or `executive_order`. `guidance` is an agency interpretation, not binding law. |
| `title`, `bill_number`, `citation` | Names and legal citations. |
| `status` | `enacted` or `final` (binding); `proposed`, `draft_guidance`, `died`, `vetoed`, `withdrawn`, `rescinded`, `vacated` (not obligations). |
| `signed_or_published_date` | When signed or published. |
| `effective_date` | When the first duty becomes enforceable. |
| `effective_date_notes` | Later phases and duty-specific deadlines. |
| `ai_specific` | Whether the law is written specifically for AI. |
| `applies_to`, `tool_categories`, `data_triggers` | Who, which kinds of tool, and which data types the law reaches. |
| `triggers`, `example_tools` | Plain-language description of when it applies, with examples. |
| `exclusions`, `key_definitions`, `key_questions` | Scope limits, definitions that matter, and the facts that would change the answer. Read these before relying on a match. |
| `obligations`, `enforcement` | What the law requires and who enforces it. |
| `primary_source_url`, `secondary_source_url` | Official text, and a backup source. |
| `verification_level` | `primary_verified`, `partially_verified`, or `unverified`. |
| `last_verified` | Date the row was last checked against its source. |
| `related_ids`, `notes` | Related rows and maintainer notes. |

## `risks-best-practices.csv`

| Column | Meaning |
|---|---|
| `risk_id` | `R-...` for a risk, `P-...` for a practice. |
| `row_type` | `risk` or `practice`. |
| `title`, `category` | Name and theme (for example `bias_fairness`). |
| `what_can_go_wrong` | The risk in plain language. |
| `trigger_explanation` | Why the rule fires. |
| `best_practices` | Recommended mitigations. |
| `lifecycle_stage` | Where in the AI lifecycle it applies. |
| `priority` | `high`, `medium`, or `low`. |
| `sources`, `source_urls` | Framework and section; links (the first is the primary citation). |
| `related_law_ids` | Laws that actually require the practice, if any. Otherwise it is only "recommended by" the framework. |
| `check_status` | `source_checked` or `unchecked`. |

## `ai-failure-examples.csv`

| Column | Meaning |
|---|---|
| `example_id` | `EX-...`. |
| `domain` | `health` or `non_health`. |
| `title`, `year`, `organizations` | The case. |
| `what_happened`, `failure_mechanism`, `lesson_for_builders` | Facts, cause, and takeaway. |
| `related_risk_ids` | Risks the case illustrates. The matcher shows a case only if its own rule matches and at least one linked risk also matches. |
| `evidence_status` | `established`, `alleged`, `settled`, or `mixed`. Never present an `alleged` fact as established. |
| `evidence_type`, `outcome` | Kind of evidence (for example `peer_reviewed`) and the organization's response or result. |
| `sources`, `source_urls` | Citations. |
| `check_status` | `source_checked` or `unchecked`. |
