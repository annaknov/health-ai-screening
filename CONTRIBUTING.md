# Contributing

Corrections to the knowledge base are the most useful contribution: a wrong effective date, a rule that fires when it shouldn't, a broken source link, or a missing law.

## Before you open a pull request

1. Run `python -m unittest discover -s tests -v`. All tests must pass.
2. For a **law or risk row**, cite a primary source in `primary_source_url` or `source_urls`, set `verification_level` or `check_status` honestly, and update `as_of`.
3. For a **new trigger_rule**, use only tags defined in `knowledge_base/tag-schema.md`. If you need a new tag, add it to the schema and to the questionnaire (so some answer can set it), and bump both version numbers and their change logs.
4. For a **new failure example**, include a source for every factual claim. Mark claims from unresolved lawsuits as `alleged`.
5. Keep `status` accurate. Only `enacted` and `final` rows are obligations.

## Style for row text

Plain language, no legal conclusions beyond what the source says. Put exemptions and thresholds the tags can't express in `exclusions` and `key_questions`, not in the rule.

## Reporting a legal error

Open an issue with the row ID, what's wrong, and a link to the primary source. This project is a screening aid and not legal advice; please don't send case-specific legal questions.
