# Intake questionnaire (v0.8)

How to run it: 7 rounds, at most 3 main questions per round; conditional follow-ups (Q1a, Q4a…) don't count toward the 3. Present every question as multiple choice, and tell the user once at the start that they can type their own answer instead of choosing an option. Ask conditional questions only when their condition holds. Skip a question entirely if Q0 already answers it clearly (set its tags as "inferred"); otherwise pre-select nothing (see Interface rules).

Each option lists the tags it sets (see `tag-schema.md`). Formatting:
- `tag` → set to yes
- `tag?` → set to unsure; evaluate both ways
- `—` → no tag

Interface rules:
- Do not label any option "recommended" or "suggested." Pre-select nothing; order options neutrally. Use Q0 only to skip questions it already answers clearly.
- Every question also accepts the user's own typed answer. Map a typed answer to the closest option's tags and mark them "inferred."
- If the interface limits a question to 4 options, split it into parts or fold the rarest options into the typed-answer box, exactly as listed in "Interface limits" at the end. Never drop an option's tags.
- After Round 7, run the consistency check (see "Consistency check") before matching.

Tags the intake never sets are **no**. If the user types a free-text answer, map it to the closest option's tags and mark those tags as "inferred" in the profile.

---

## Opening (free text, before Round 1)
**Q0.** In 2–3 sentences, describe your tool: what it does, who uses it, and what problem it solves.
→ No tags are set directly. Use the answer to pre-select likely options in later rounds, and quote it in the report.

## Round 1: Organization and purpose
**Q1. Which describes your organization? (select all that apply)**
Select Provider or Health plan only if your organization is one itself. If you build or sell the tool to providers, plans, or employers, select "Company building AI for others to use" and not Provider or Plan.

| Option | Tags |
|---|---|
| Provider: hospital, clinic, or medical practice (we deliver care ourselves) | `org_provider` |
| Health plan or insurer (we are the plan ourselves) | `org_plan` |
| Company building AI for others to use (a vendor to providers, health plans, or employers) | `org_developer` |
| Consumer health app or service | `org_consumer_business` |
| Government agency or public health system | `org_government` |
| Platform or device company: hosts AI models for download, runs a content platform with 2M+ monthly users, or makes cameras or recorders | `provenance_actor` |

**Q1a (conditional: `org_plan`, `org_developer` with Q2 including coverage/prior authorization, or Q2 includes coverage/prior authorization). Which health plan lines of business will use it, yours or your customers'? (select all that apply)**
| Option | Tags |
|---|---|
| Medicare Advantage | `plan_medicare_advantage` |
| Medicaid or CHIP managed care | `plan_medicaid_chip` |
| ACA Marketplace | `plan_marketplace` |
| Traditional Medicare fee-for-service (e.g., as a CMS contractor or model participant, or a provider submitting prior auth) | `medicare_ffs` |
| Commercial or employer plans only | — |

**Q1b (conditional: `org_developer`). Does your company have any ONC-certified health IT product (for example a certified EHR module)?**
| Option | Tags |
|---|---|
| Yes, and this tool ships inside it | `certified_developer` `certified_health_it` |
| Yes, but this tool is separate | `certified_developer` |
| No | — |
| Not sure | `certified_developer?` `certified_health_it?` |

**Q1c (conditional: `org_plan`, or `org_developer` with Q1a answered). In California, how is the plan licensed (yours or your customers')?**
| Option | Tags |
|---|---|
| Department of Insurance health insurer (a "disability insurer" selling health insurance) | `plan_doi_insurer` |
| Department of Managed Health Care (Knox-Keene plan, HMO) | — |
| Both, or not sure | `plan_doi_insurer?` |
| No California plans | — |

**Q1d (conditional: any Q1 answer other than "Consumer health app" alone). Does your organization run a health information network or exchange, moving health data among more than two unaffiliated organizations (for example an HIE, a national network, or a data-sharing platform between providers and plans)?**
| Option | Tags |
|---|---|
| Yes | `hin_hie` |
| No | — |
| Not sure | `hin_hie?` |

**Q2. What does the tool do? (select all that apply)**
| Option | Tags |
|---|---|
| Supports clinical decisions (diagnosis, treatment, triage, risk scores) | `cdss` |
| Writes to or talks with patients or members | `patient_comm` |
| Coverage, prior authorization, or medical necessity | `utilization_review` |
| Delivers treatment or therapy directly to users (e.g., a CBT program) | `digital_therapeutic` |
| Mental health or emotional support | `mental_health_use` |
| Decisions about staff (hiring, scheduling, performance) | `workforce_decisions` |
| Drafts notes, summaries, or documentation for clinicians | `drafts_clinical_documentation` |
| Administrative only (scheduling, coding, documentation) | `admin_only` |

**Q3. What stage is it at?**
| Option | Tags |
|---|---|
| Idea or design | `stage_pre_deploy` |
| Building or testing | `stage_pre_deploy` |
| Piloting with real users | `stage_live` |
| Fully deployed | `stage_live` |

## Round 2: Model and data
**Q4. What kind of model is it?**
| Option | Tags |
|---|---|
| Generative AI / LLM (writes text, summarizes, chats) | `genai` |
| Predictive model (scores, classifications, risk predictions) | `predictive_ml` |
| Rules-based logic | — |
| A chatbot, but not sure whether it uses a large language model | `genai?` |
| A combination | `genai?` `predictive_ml?` (follow up: which parts) |

**Q4a (conditional: `genai` or `genai?`). Does it generate images, audio, or video, including a synthetic voice?**
| Option | Tags |
|---|---|
| Yes | `generates_media` |
| No, text only | — |

**Q5. What is it built on?**
| Option | Tags |
|---|---|
| Our own model, trained on our data | — |
| A vendor or foundation model used as-is (e.g., GPT, Claude, an EHR vendor model) | `third_party_model` |
| A vendor or foundation model that we fine-tune | `third_party_model` `trains_genai_model?` |
| Our own foundation model trained at frontier scale (over 10^26 operations) | `trains_genai_model` `frontier_model` |
| Not sure | `third_party_model?` |

**Q6. What data goes in? (select all that apply)**
| Option | Tags |
|---|---|
| Medical records or claims from a provider, plan, or other HIPAA-covered organization | `phi` |
| Substance use disorder treatment records | `phi` `substance_use_records` |
| Health data people enter themselves, or from devices or wearables | `consumer_health_data` |
| Brain or nervous-system signals (EEG, neurotech devices) | `neural_data` |
| Other personal data (contact info, behavior, marketing data) | `other_personal_info` |
| No personal or health data | — |

**Q6a (conditional: any personal or health data). Will any of that data be sold, shared for advertising, or reused to train other products?**
| Option | Tags |
|---|---|
| Yes | `shares_personal_data` |
| Yes, and selling or sharing personal data brings in half or more of our revenue | `shares_personal_data` `data_seller` |
| No | — |
| Not sure | `shares_personal_data?` |

**Q6b (conditional: `consumer_health_data` or `org_consumer_business`). Does the product keep people's medical information so they or their providers can use it, or offer mental-health or reproductive/sexual-health services?**
| Option | Tags |
|---|---|
| Yes | `cmia_digital_service` |
| No | — |
| Not sure | `cmia_digital_service?` |

## Round 3: What the model learns from
**Q7. Does the model use any of these as inputs? (select all that apply)**
| Option | Tags |
|---|---|
| Race, ethnicity, sex, age, or language | `uses_demographics` |
| Zip code, income, or insurance type | `uses_ses_proxy` |
| Past costs or service use | `uses_cost_utilization` |
| None of these | — |

**Q8. What is it trained to predict or optimize?**
| Option | Tags |
|---|---|
| A directly measured clinical outcome (diagnosis, lab value, event) | — |
| A stand-in measure (cost, service use, billing codes, past staff decisions) | `proxy_outcome_label` |
| We didn't train it (off-the-shelf model) | `third_party_model` |
| Not sure | `proxy_outcome_label?` |

**Q9. After launch, will the model be retrained, fine-tuned, or swapped for a newer version?**
| Option | Tags |
|---|---|
| Yes, planned | `model_updates_planned` |
| Possibly (e.g., the vendor updates it) | `model_updates_planned?` |
| No, it stays fixed | — |

## Round 4: Outputs and who sees them
**Q10. Who sees the output first?**
| Option | Tags |
|---|---|
| A clinician | — |
| Other staff (care manager, reviewer, admin) | — |
| The patient or consumer directly | `patient_facing` |

**Q11. Does the output include information about a specific person's health?**
| Option | Tags |
|---|---|
| Yes | `clinical_info_comm` |
| Sometimes | `clinical_info_comm?` |
| No | — |

**Q12 (conditional: `patient_facing` or `patient_comm`). Before a patient sees it, does a licensed clinician read and review it?**
| Option | Tags |
|---|---|
| Always | `clinician_review` |
| Sometimes | `clinician_review?` |
| Never | — |

## Round 5: Human control and interaction
**Q13. Who makes the final decision or takes the final action?**
| Option | Tags |
|---|---|
| A person decides; the tool only informs | — |
| A person approves the tool's suggested default | `automation_bias_risk` |
| The tool acts automatically | `automated_significant_decision` `autonomy_high` |

If the answer differs by outcome (for example, a person makes every denial but approvals go through automatically), ask which outcomes the tool handles without a person, and set `automated_significant_decision?` and `autonomy_high?` if any do or it is unclear.

**Q14. How does it interact with people? (select all that apply)**
| Option | Tags |
|---|---|
| Not conversational | — |
| Task-focused chat (answers questions, schedules) | `chatbot` |
| Open-ended chat that could become ongoing or supportive | `chatbot` `companion_capable` |
| Records or transcribes live conversations (visits, calls) | `records_conversations` |
| Makes phone calls or sends texts automatically, or speaks with an AI voice | `outbound_calls_texts` |

**Q15. How is it presented to users?**
| Option | Tags |
|---|---|
| Product name only | — |
| A human first name or persona | `implies_licensure?` |
| A clinical title or "care team" language (e.g., "Nurse Ava") | `implies_licensure` |

Follow-up (free text): "What is the name or persona?"

## Round 6: Regulatory path and reach
**Q16 (conditional: `cdss` or `digital_therapeutic`). Do you plan to seek FDA clearance or approval?**
| Option | Tags |
|---|---|
| Yes | `fda_pathway` |
| No, we don't think it's a medical device | — |
| Not sure | `fda_pathway?` |

**Q16a (conditional: `cdss`). Which of these apply? (select all that apply)**
| Option | Tags |
|---|---|
| Analyzes medical images (X-ray, CT, MRI, ultrasound, pathology slides) | `analyzes_medical_images` `analyzes_images_signals` |
| Analyzes waveforms (ECG, EEG), lab-instrument signals, or continuous or repeated vitals | `analyzes_images_signals` |
| Users can't see the data and reasoning behind a recommendation | `basis_not_reviewable` |
| Used for urgent, time-critical decisions | `time_critical` |
| None of these | — |

**Q17. Where will it be used, and how widely?**
| Option | Tags |
|---|---|
| Outside California only | — |
| In California, under ~100,000 people a year | `ca_users` |
| In California, 100,000+ people a year | `ca_users` `ca_100k` |
| In California, 1M+ users a month | `ca_users` `large_scale` `ca_100k` |
| Not sure yet | `ca_users?` |

**Q18. What is your organization's annual revenue?**
| Option | Tags |
|---|---|
| Under $26.6 million | — |
| $26.6–500 million | `revenue_over_ccpa` |
| Over $500 million | `large_enterprise` `revenue_over_ccpa` |
| Not sure / prefer not to say | `large_enterprise?` `revenue_over_ccpa?` |

## Round 7: Users and safeguards
**Q19. Could anyone under 18 use it?**
| Option | Tags |
|---|---|
| Yes, including children under 13 | `minors_possible` `under_13_possible` |
| Yes, teens 13–17 only | `minors_possible` |
| No | — |
| Not sure | `minors_possible?` `under_13_possible?` |

**Q20. Has performance been tested across patient subgroups (race, sex, age, language, payer)?**
| Option | Tags |
|---|---|
| Yes, on our own patient population | — |
| Overall accuracy only | `subgroup_eval_missing` |
| Only the vendor's reported results | `local_validation_missing` `subgroup_eval_missing?` |
| Not yet | `local_validation_missing` `subgroup_eval_missing` |

**Q21. Is there a monitoring plan after launch (performance, drift, subgroup gaps, incidents)?**
| Option | Tags |
|---|---|
| Yes, with a named owner and metrics | — |
| Partial | `monitoring_missing?` |
| None yet | `monitoring_missing` |

---

## Consistency check (run after Round 7, before matching)
Look for conflicting answers and ask the user to resolve each one in a single multiple-choice question. Do not guess silently. Common conflicts:
- Q13 "tool acts automatically" with Q12 "clinician always reviews": ask which outcomes run without a person.
- Q14 chat or companion answers with Q4 "predictive" or "rules-based" only: ask whether any part generates text.
- Q5 "we fine-tune" with Q4 "rules-based": ask what is fine-tuned.
- Q1 Provider or Plan with a vendor-style description in Q0, or Q1a plan lines without Q1 Plan or Provider: ask whether they run the tool themselves or sell it to others.
- Q10 "patient first" with Q12 "clinician always reviews": ask which output the clinician reviews.
If the user doesn't resolve a conflict, set the affected tags to unsure and say so in the report.

## Interface limits (4 options per question)
- Q1: show Provider, Health plan, Company building AI for others, Consumer health app. Government agency and Platform or device company go in the typed-answer box.
- Q2: show as two parts. Part 1: clinical decisions, writes to patients or members, coverage or prior authorization, treatment delivery. Part 2: mental health support, staff decisions, drafts notes or documentation, administrative only. Allow part 2 to be left blank.
- Q1a: show the four plan lines; "commercial or employer plans only" is the typed-answer box or leaving it blank.
- Q6: show medical records or claims, substance use disorder records, health data people enter, other personal data. Brain signals and "no personal data" go in the typed-answer box.
- Q14: show task-focused chat, open-ended chat, records conversations, automated calls or texts. "Not conversational" is leaving it blank.
- Q4: show generative AI, predictive model, a combination, and chatbot-not-sure. "Rules-based logic" goes in the typed-answer box.
- Q16a: show the four signal and basis options; "None of these" is leaving it blank.
- Q17: show the four reach options. "Not sure yet" goes in the typed-answer box.
- Questions with 4 or fewer options are shown as written.

## Derived tags (set automatically after intake; never ask about them)
| Tag | Rule |
|---|---|
| `patient_facing` | Also set if `patient_comm` and Q10 ≠ patient (patients receive the output later in the flow) |
| `admin_only` cancels `cdss` | Only if the user selected Administrative alone in Q2 (drafting notes or documentation does not cancel it, and does not set `cdss` either) |
| `health_info` | `phi` OR `consumer_health_data` OR `substance_use_records` OR `neural_data` |
| `non_hipaa_personal_info` | `consumer_health_data` OR `neural_data` OR `other_personal_info` |
| `hipaa_entity` | yes if `phi` (a covered entity, or a vendor receiving PHI from one, which is almost always a business associate); unsure if `org_provider` or `org_plan` without `phi`. Label as inference in the report. |
| `hhs_funded` | yes if `plan_medicare_advantage`, `plan_medicaid_chip`, or `plan_marketplace` (not `plan_doi_insurer`); unsure if `org_provider` (most providers accept Medicare or Medicaid) or `org_developer` (customers are usually providers or plans that do). Label as inference. |
| `ccpa_business` | `ca_users` AND NOT `org_government` AND (`revenue_over_ccpa` OR `data_seller` OR (`ca_100k` AND `shares_personal_data`)), evaluated with unsure values (Civ. Code 1798.140(d)(1): revenue over $26,625,000; buys, sells, or shares data on 100,000+ consumers or households; or half of revenue from selling or sharing) |
| `large_genai_platform` | `genai` AND `generates_media` AND `large_scale` |
| `possible_device` | (`cdss` AND (`fda_pathway` OR `analyzes_images_signals` OR `patient_facing` OR `time_critical` OR `basis_not_reviewable`)) OR `digital_therapeutic` OR `fda_pathway` |
| `minors_possible` | Also set if `under_13_possible` |

## Changes from v0.7 (2026-10-12, independent review)
- Q1: new option for model-hosting, large content platforms, and recording-device makers (`provenance_actor`, AB 853). Interface: typed-answer box.
- Q1b now asks about the company (any certified product → `certified_developer`), not only this tool (information blocking covers any developer of certified health IT).
- Q5: new option for frontier-scale training (`frontier_model`, SB 53).
- Q6a: new option for companies earning half their revenue from selling or sharing data (`data_seller`, CCPA).
- New Q6b (conditional): CMIA-covered digital services (`cmia_digital_service`): medical-record apps, mental-health and reproductive/sexual-health services.
- Q17/Q18 now set `ca_100k` and `revenue_over_ccpa` (threshold corrected to $26.6M); `ccpa_business` is derived from the three statutory routes.
- Pairs with `tag-schema.md` v0.7.

## Changes from v0.6 (2026-10-10, external audit fixes)
- New Q1c (plan licensing in California → `plan_doi_insurer`) for SB 354, which covers DOI-licensed health insurers but not Knox-Keene plans.
- New Q1d (health information network or exchange → `hin_hie`) for the information blocking rule. Asked unless the user is only a consumer app; a conditional follow-up, so it does not count toward the 3 main questions per round.
- Pairs with `tag-schema.md` v0.6.

## Changes from v0.5 (2026-10-08, merge)
- Merged the Project's v0.5 with the Claude Code master (v0.3 + fixes); this file is now the single master.
- Derived `hhs_funded` is now unsure for vendors (`org_developer`), per Anna's A7 decision; the 1557, 92.210, and 84.84 rules no longer have vendor branches, so they show "depends on your customers taking HHS funding."
- Removed the conflict between "pre-select likely options" (header) and "pre-select nothing" (interface rules): nothing is pre-selected.
- Q4 now has 5 options, so it gets an interface-limit entry.
- Q16a splits images from other signals (new tag `analyzes_medical_images`), so image-only FDA classifications don't match vital-sign models.
- `intended_user_patient`: decided not to add (`patient_facing` already covers it).
- Pairs with `tag-schema.md` v0.5.

## Changes from v0.4 (2026-10-08)
- New Q2 option "Drafts notes, summaries, or documentation for clinicians" sets new tag `drafts_clinical_documentation` (added to `tag-schema.md` v0.4).
- New Q4 option "A chatbot, but not sure whether it uses a large language model" sets `genai?`.
- Q16a first option now includes continuous or repeated vitals, matching FDA's CDS guidance.
- New interface rules: no "recommended" labels, nothing pre-selected, typed answers always allowed.
- New consistency check after Round 7, and a list of how to fit questions into 4 options.
- Not changed, pending decisions: `intended_user_patient` tag; unsure `hhs_funded` for developers (both resolved in v0.6).

## Changes from v0.3 (2026-10-08)
- Q18 "Not sure / prefer not to say" now also sets `ccpa_business?` (before, an unknown revenue silently meant CCPA did not apply).
- Q1 now says to pick Provider or Plan only if the organization is one itself; vendors pick "Company building AI for others to use" only. Q1a now also asks vendors that touch coverage or prior authorization which plan lines their customers run.
- Q13 now has a follow-up for tools where a person decides some outcomes (for example denials) but not others (for example approvals).
- `tag-schema.md` is unchanged (still v0.3); no new tags.

## Changes from v0.2 (2026-10-07)
- New options and follow-ups so every law's trigger can be expressed in tags: plan lines of business (Q1a), certified health IT (Q1b), mental health and workforce uses (Q2), media generation (Q4a), specific data types (Q6), data sharing (Q6a), recording and automated calls (Q14), FDA pathway facts (Q16/Q16a), California reach (Q17), revenue (Q18), under-13 users (Q19).
- New Q9 (model updates after launch) for drift and change-control risks.
- Round 6 previously had 4 questions; questions are now spread over 7 rounds. Net user burden: 18 → 21 main questions, plus up to 6 conditional follow-ups.
