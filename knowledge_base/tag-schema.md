# Tag schema (v0.7)

Intake answers set tags (see `intake-questionnaire.md`). Every law row (`california-laws.csv`, `federal-laws.csv`) and every risk row (`risks-best-practices.csv`) has a `trigger_rule` written in these tags. This file is the only list of valid tags; the validator rejects any other name.

## Rules
- Syntax: tag names joined with `AND` / `OR` / `NOT`, parentheses for grouping. `ALWAYS` applies to every tool.
- Tag values: **yes**, **no**, **unsure**. A tag the intake never set is **no**, unless the user's Q0 description clearly says otherwise (then set it and mark it "inferred").
- Evaluating with unsure tags: evaluate the rule with each unsure tag as yes and as no.
  - True either way → **Applies**.
  - True only for some values → **Possibly applies**; name the unsure fact(s) as "conditional on …".
  - False either way → **Not applicable**.
- `NOT x` is true only when x = no. So `NOT clinician_review` with clinician_review = unsure gives "Possibly applies, conditional on clinician review."
- Developers: when a law binds the organizations that deploy a tool (providers, plans), its rule also includes `org_developer`, because a vendor's customers carry the obligation and the product must support it. Reports say "applies to your customers" in that case.
- Derived tags are computed with the same three-valued logic (e.g., `possible_device` is unsure if it depends on an unsure answer).
- Rules state when a row is in scope. Thresholds and exemptions the tags can't capture stay in the row's prose (`exclusions`, `key_questions`), and the report says so.

## Organization
| Tag | Meaning | Set by |
|---|---|---|
| `org_provider` | Health facility, clinic, physician office, group practice, or other health care provider builds or deploys the tool | Q1 |
| `org_plan` | Health plan, HMO, or health/disability insurer | Q1 |
| `org_developer` | Builds AI for other organizations to deploy | Q1 |
| `org_consumer_business` | Offers the tool directly to consumers, outside a provider or plan relationship | Q1 |
| `org_government` | Government agency or public health system | Q1 |
| `plan_medicare_advantage` | Plan offers Medicare Advantage | Q1a |
| `plan_medicaid_chip` | Plan offers Medicaid or CHIP managed care | Q1a |
| `plan_marketplace` | Plan offers ACA Marketplace coverage | Q1a |
| `medicare_ffs` | Works on traditional Medicare fee-for-service prior authorization or claims (provider, CMS contractor, or model participant) | Q1a |
| `certified_health_it` | Tool ships in, or as part of, an ONC-certified health IT product (e.g., an EHR) | Q1b |
| `certified_developer` | The company has any ONC-certified health IT product, whether or not this tool is part of it | Q1b |
| `provenance_actor` | Hosts AI models for download, runs a content platform with 2M+ monthly users, or makes cameras or recorders (AB 853 actors) | Q1 |
| `plan_doi_insurer` | Plan is (or, for a vendor, its customer is) a California Department of Insurance-licensed health insurer, not a Knox-Keene (DMHC) plan | Q1c |
| `hin_hie` | Organization runs a health information network or exchange: moves health data among more than two unaffiliated organizations for treatment, payment, or operations (45 CFR 171.102) | Q1d |
| `hhs_funded` | The organization, or for a vendor its customers, receives HHS funding (e.g., Medicare, Medicaid) or runs an HHS program | Derived |
| `hipaa_entity` | HIPAA covered entity, or business associate handling PHI for one | Derived |

## Use and function
| Tag | Meaning | Set by |
|---|---|---|
| `cdss` | Prediction, classification, recommendation, or analysis that aids decisions on timing of care, diagnosis, or treatment | Q2 |
| `patient_comm` | Generates or sends communications to patients or members | Q2 |
| `utilization_review` | Prior authorization, medical necessity, or coverage decisions | Q2 |
| `drafts_clinical_documentation` | Drafts clinical notes, visit summaries, or other documentation for clinicians (with or without their review) | Q2 |
| `admin_only` | Scheduling, coding, billing, or documentation with no clinical judgment | Q2 |
| `digital_therapeutic` | Delivers treatment or therapy directly to the user (e.g., a CBT program, digital therapeutic) | Q2 |
| `mental_health_use` | Mental health, emotional support, or behavioral health use | Q2 |
| `workforce_decisions` | Used for decisions about workers (hiring, scheduling, evaluation, discipline) | Q2 |
| `stage_pre_deploy` | Idea, design, building, or testing | Q3 |
| `stage_live` | Piloting with real users or fully deployed | Q3 |

## Model
| Tag | Meaning | Set by |
|---|---|---|
| `genai` | Generative AI produces text, audio, images, or video | Q4 |
| `predictive_ml` | Statistical or ML model that produces scores or classifications | Q4 |
| `generates_media` | GenAI output includes images, audio, or video (including synthetic voice) | Q4a |
| `third_party_model` | Relies on a vendor or foundation model | Q5, Q8 |
| `trains_genai_model` | Trains or fine-tunes a generative model that others use | Q5 |
| `frontier_model` | Trains a frontier-scale model (>10^26 operations) | Q5 |
| `uses_demographics` | Race, ethnicity, sex, age, or language used as inputs | Q7 |
| `uses_ses_proxy` | Zip code, income, or insurance type used as inputs | Q7 |
| `uses_cost_utilization` | Past cost or utilization used as inputs | Q7 |
| `proxy_outcome_label` | Target is a stand-in (cost, utilization, codes, past decisions) rather than a direct health measure | Q8 |
| `model_updates_planned` | Model will be retrained, fine-tuned, or swapped after launch | Q9 |

## Data
| Tag | Meaning | Set by |
|---|---|---|
| `phi` | Medical records or claims from a provider, plan, or other HIPAA-covered organization | Q6 |
| `consumer_health_data` | Health data people enter themselves or from devices/wearables, outside HIPAA | Q6 |
| `substance_use_records` | Substance use disorder treatment records | Q6 |
| `neural_data` | Brain or nervous-system signals (EEG, neurotech) | Q6 |
| `other_personal_info` | Other personal data (contact, behavior, marketing) | Q6 |
| `health_info` | Any health information | Derived |
| `non_hipaa_personal_info` | Personal information outside HIPAA coverage | Derived |
| `shares_personal_data` | Personal data sold, shared for advertising, or reused to train other products | Q6a |
| `data_seller` | Half or more of revenue comes from selling or sharing personal data | Q6a |
| `cmia_digital_service` | Keeps people's medical information for them or their providers, or offers mental-health or reproductive/sexual-health digital services (Civ. Code 56.06(b), (d), (e)) | Q6b |

## Outputs and human control
| Tag | Meaning | Set by |
|---|---|---|
| `patient_facing` | Output reaches patients or consumers | Q10, derived |
| `clinical_info_comm` | Output contains information about a specific person's health status | Q11 |
| `clinician_review` | A licensed clinician reads and reviews patient-facing output before it is sent | Q12 |
| `automation_bias_risk` | A human approves the tool's default, so rubber-stamping is likely | Q13 |
| `automated_significant_decision` | Replaces or substantially replaces human decision-making on care, coverage, employment, or health assessment | Q13 |
| `autonomy_high` | Tool acts without a human approving each action | Q13 |

## Interaction
| Tag | Meaning | Set by |
|---|---|---|
| `chatbot` | Conversational, natural-language interface | Q14 |
| `companion_capable` | Can sustain relational or emotionally supportive conversation, whether or not designed to | Q14 |
| `records_conversations` | Records, transcribes, or listens to live conversations (visits, calls) | Q14 |
| `outbound_calls_texts` | Places AI-voiced, prerecorded, or autodialed calls or automated texts | Q14 |
| `implies_licensure` | Name, persona, title, or design could suggest a licensed clinician | Q15 |

## FDA pathway (asked only if `cdss` or `digital_therapeutic`)
| Tag | Meaning | Set by |
|---|---|---|
| `fda_pathway` | Plans to seek FDA clearance, De Novo, or approval | Q16 |
| `analyzes_images_signals` | Analyzes medical images, waveforms (ECG, EEG), lab-instrument signals, or continuous or repeated vital signs | Q16a |
| `analyzes_medical_images` | Analyzes medical images (X-ray, CT, MRI, ultrasound, pathology slides); also sets `analyzes_images_signals` | Q16a |
| `basis_not_reviewable` | Users can't see the data and reasoning behind a recommendation well enough to check it independently | Q16a |
| `time_critical` | Used for urgent or time-critical decisions | Q16a |
| `possible_device` | Could be an FDA-regulated device: (`cdss` AND (`fda_pathway` OR `analyzes_images_signals` OR `patient_facing` OR `time_critical` OR `basis_not_reviewable`)) OR `digital_therapeutic` OR `fda_pathway` | Derived |

## Reach and scale
| Tag | Meaning | Set by |
|---|---|---|
| `ca_users` | Used in California or by Californians | Q17 |
| `large_scale` | 1M+ monthly users | Q17 |
| `ca_100k` | Reaches 100,000+ people in California a year | Q17 |
| `revenue_over_ccpa` | Annual revenue over $26,625,000 (CCPA threshold, CPI-adjusted 2025) | Q18 |
| `ccpa_business` | Meets a CCPA "business" route: `ca_users` AND NOT `org_government` AND (`revenue_over_ccpa` OR `data_seller` OR (`ca_100k` AND `shares_personal_data`)) | Derived |
| `large_enterprise` | Over $500M national annual revenue (AB 1609, SB 53 thresholds) | Q18 |
| `large_genai_platform` | GenAI that generates media, with 1M+ monthly users | Derived |
| `minors_possible` | Users under 18 plausible | Q19 |
| `under_13_possible` | Users under 13 plausible (COPPA) | Q19 |

## Safeguards (mostly for risks and best practices)
| Tag | Meaning | Set by |
|---|---|---|
| `local_validation_missing` | Not validated on the deploying population | Q20 |
| `subgroup_eval_missing` | No performance comparison across subgroups | Q20 |
| `monitoring_missing` | No post-launch monitoring plan | Q21 |

## Changes from v0.6 (2026-10-12, independent review)
- Added `certified_developer`, `provenance_actor`, `data_seller`, `cmia_digital_service`, `ca_100k`, `revenue_over_ccpa`. `frontier_model` is now asked (Q5). `ccpa_business` is derived from the three statutory routes instead of user count.
- Pairs with `intake-questionnaire.md` v0.8.

## Changes from v0.5 (2026-10-10, external audit fixes)
- Added `plan_doi_insurer` (Q1c): SB 354 covers DOI-licensed health insurers despite its HIPAA exemption (Ins. Code 791.01(e)(4)), but not Knox-Keene plans. Without this tag the rule could not match any plan.
- Added `hin_hie` (Q1d): health information networks and exchanges are information-blocking actors (45 CFR 171.102) even when they are not providers or certified developers.
- Pairs with `intake-questionnaire.md` v0.7.

## Changes from v0.4 (2026-10-08, merge)
- Merged the Project's v0.4 and the Claude Code v0.4, which made the same two tag changes; this file is now the single master. Content is the union: `drafts_clinical_documentation`, wider `analyzes_images_signals`, `hhs_funded` unsure for vendors, `intended_user_patient` not added.
- Added `analyzes_medical_images`: once `analyzes_images_signals` grew to include vital signs, image-only FDA classifications (CADE, MLQI) matched a sepsis model. Those rules now use the image tag.
- Pairs with `intake-questionnaire.md` v0.6.

## Changes from v0.3 (2026-10-08)
- Added `drafts_clinical_documentation` (Q2), so documentation risks no longer fire for chatbots that write no notes.
- `analyzes_images_signals` now includes continuous or repeated vital signs (FDA CDS guidance treats them as signals).
- `hhs_funded` is now unsure for vendors (`org_developer`), whose customers usually take Medicare or Medicaid; the HHS-funding law rules no longer have separate vendor branches.
- Considered and not added: `intended_user_patient`; `patient_facing` already captures the intended-user test in `possible_device`.

## Changes from v0.2 (2026-10-07)
- Location-neutral org tags (federal laws use them too); California reach is now its own tag, `ca_users`.
- Added tags the law rows need: `hipaa_entity`, `hhs_funded`, plan lines of business, `certified_health_it`, `phi` / `consumer_health_data` / `substance_use_records` / `neural_data`, `records_conversations`, `outbound_calls_texts`, `mental_health_use`, `workforce_decisions`, `generates_media`, `ccpa_business`, `under_13_possible`, `org_government`, `frontier_model`.
- Added FDA device-status facts (`fda_pathway`, `analyzes_images_signals`, `basis_not_reviewable`, `time_critical`); `cdss` alone does not decide device status.
- Added `model_updates_planned` (drift, change control). Split the stage tags into two rows.
- `health_info` and `non_hipaa_personal_info` are now derived from the specific data tags.
- Added `medicare_ffs` (CMS WISeR) and `digital_therapeutic` (FDA device status for treatment apps).
- `large_enterprise` defined as >$500M revenue (AB 1609).
