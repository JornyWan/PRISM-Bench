# PRISM-Bench: Release Notes & Incident Archive

**Date:** March 2026

We appreciate the community's feedback and the scrutiny that helps improve benchmarks. Following recent discussions regarding data quality and our codebase, we temporarily paused some tracks for active repair. 

We are pleased to announce that **the data has been fully repaired and re-released**. Below is a detailed archive addressing the past issues and the steps we took to resolve them.

---

### 1. Regarding the Inference Code Bug

There was a misunderstanding regarding a bug in our repository. The issue involving incorrect image loading was isolated strictly to the `example_inference.py` demonstration script, which was provided solely for community reference. Each MLLM has its own way of loading input data; we only provided one example script to demonstrate how to load and use our benchmark.

* **Paper Integrity:** All experiments and results reported in the paper were conducted using our internal evaluation pipeline, which correctly loads and processes all visual data.
* **Evidence:** As demonstrated in the paper’s appendix, the models successfully interpret and describe visual content, confirming they had full access to the images during our evaluations.
* **Status:** The demo script has been fixed to correctly reflect the intended usage.

### 2. Regarding Data Quality & CoT Traces

We acknowledge an oversight in our initial data pipeline. While we manually inspected the injected errors, we relied on GPT-4 to convert ground-truth solutions into step-by-step Chain-of-Thought (CoT) traces. We underestimated the hallucination rate during this transformation and did not audit the CoT steps as rigorously as required.

* **Resolution:** We have conducted a systematic, exhaustive manual review of all CoT traces. All labeling errors and hallucinations have been corrected in the current release.

### 3. Community Engagement & Communication

We would also like to address the interaction on our GitHub Issues. While our initial response provided detailed technical context, we acknowledge that closing the issue prematurely marked it as 'resolved' too soon. 

However, it is important to clarify the timeline: **We actually reopened the issue and provided a second, even more detailed response three weeks prior to the wider social media discussions**, immediately after the user requested it. We have kept the issue open since then to ensure all follow-up questions are thoroughly resolved. 

We highly value constructive feedback and remain committed to an open dialogue with the research community. Thank you for helping us make PRISM-Bench better.
