# IMDRF Good Machine Learning Practice: guiding principles (summary)

Source: IMDRF/AIML WG/N88 FINAL, *Good machine learning practice for medical device development: Guiding principles*, 27 January 2025. https://www.imdrf.org

This is a paraphrased summary for screening use, not the IMDRF text, and it is not endorsed by IMDRF. The original is copyrighted by IMDRF; download it from the IMDRF website. The principles are a call to action for standards bodies and regulators, not binding law. Cite them as "recommended by IMDRF GMLP, Principle N."

The document also notes that generative AI raises the stakes: products may build on foundation models outside the manufacturer's control, and demonstrating performance is harder.

| # | Principle | In short |
|---|---|---|
| 1 | Intended use is well understood; multi-disciplinary expertise throughout the life cycle | Know the clinical context, workflow, benefits, and patient risks, and involve the right experts from start to finish. |
| 2 | Good software engineering, device design, and security practices | Data quality, data management, cybersecurity, risk management, traceability and reproducibility, and planning for deployment, monitoring, and maintenance. |
| 3 | Clinical evaluation uses datasets representative of the intended population | Training, test, and monitoring data should reflect the patients, sites, and inputs the tool will meet, to manage bias and drift and to find subgroups where it underperforms. |
| 4 | Training data are independent of test sets | Address every source of dependence (patients, sites, acquisition); external validation proportionate to risk. |
| 5 | Reference standards are fit for purpose | Document why the chosen ground truth suits the intended use and understand its limits; use accepted standards where they exist. |
| 6 | Model choice and design fit the data and intended use | Show the design suits the data and mitigates overfitting, degradation, and security risks; set clinically meaningful performance goals that consider subgroups and uncertainty. |
| 7 | Assess the human-AI team, not the device in isolation | Test in the real workflow, including user skill, understanding of limits, overreliance, autonomy level, and foreseeable misuse. |
| 8 | Testing shows performance under clinically relevant conditions | Sound test plans, independent of training data, covering population, subgroups, environment, and confounders. |
| 9 | Users get clear, essential information | Intended use, benefits and risks, subgroup performance, data and study description, acceptable inputs, limitations, basis for outputs where possible, update timing, and a way to report concerns. |
| 10 | Monitor deployed models; manage retraining risks | Risk-based real-world monitoring; controls against overfitting, new bias, and drift when models are retrained. |
