<!-- Top-centered logo -->
<p align="center">
  <a href="https://github.com/JornyWan/PRISM-Bench">
    <img src="assets/prism_logo.png" alt="PRISM-Bench" width="420">
  </a>
</p>

# PRISM-Bench

This repository contains the code and data for **PRISM-Bench**, a benchmark designed to evaluate multimodal large language models (MLLMs) on **reasoning with complex visual puzzle**.

A subset of first-error-detection track is under active repair. **We will release our data again after fixed!**

---

# **Clarification and Updates regarding PRISM-Bench**

We appreciate the community's feedback and the scrutiny that helps improve benchmarks. We would like to address recent questions regarding data quality and the codebase:

**1. Regarding the Inference Code Bug**
There has been a misunderstanding regarding a bug in our repository. The issue involving incorrect image loading was isolated to the `example_inference.py` demonstration script provided for community reference. Each MLLM has its own way to load input data; we only provide one example script for the purpose of showing how to load and use our benchmark.

&nbsp;&nbsp;&nbsp;&nbsp;**1.1 Paper Integrity:** All experiments and results reported in the paper were conducted using our internal evaluation pipeline, which correctly loads and processes all visual data.

&nbsp;&nbsp;&nbsp;&nbsp;**1.2 Evidence:** As demonstrated in the paper’s appendix, the models successfully interpret and describe visual content, which confirms they had full access to the images.

&nbsp;&nbsp;&nbsp;&nbsp;**1.3 Status:** The demo script has been fixed to correctly reflect the intended usage.
     
**2. Regarding Data Quality & CoT Traces** We acknowledge an oversight in our data pipeline. While we manually inspected the injected errors, we relied on GPT-4 to convert ground-truth solutions into step-by-step Chain-of-Thought (CoT) traces. We underestimated the hallucination rate during this transformation and did not audit the CoT steps as rigorously as required.

&nbsp;&nbsp;&nbsp;&nbsp;**2.1 Action Plan:** We are currently conducting a systematic manual review of all CoT traces to correct these labeling errors.
     
**3. Community Engagement** We would also like to address the interaction on GitHub. While our initial response provided detailed technical context, we acknowledge that closing the issue prematurely marked it as 'resolved' too soon.
However, it is important to clarify the timeline: **We actually reopened the issue and provided a second, even more detailed response three weeks ago (well before the recent social media discussions)** immediately after the user requested it. We have kept the issue open since then to ensure all follow-up questions are thoroughly resolved. We value constructive feedback and remain committed to an open dialogue.

## 🚀 Features

- **Diverse Visual Reasoning Tasks**: puzzles, graph-based reasoning, pattern recognition, algorithmic reasoning, etc.  
- **Chain-of-Thought (CoT) Annotations**: ground-truth reasoning steps for each problem.
- **Instruction Corruption**: synthetic corrupted reasoning chains for robustness testing.  
- **First-Error Detection**: annotations for the first mistake in incorrect reasoning chains.   
- **VQA-Style Evaluation**: multiple-choice format with definitive ground-truth answers.
  

## 📊 Dataset Format

Each entry in the benchmark is stored as a JSON object:

```
{
  "id": 2,
  "image_url": "https://example.com/images/question_0002.png",
  "question_text": "Figure Reasoning",
  "answer": "D",
  "groundtruth_cot": "Step 1) ... Step 2) ... Step 3) ...",
  "cot_corrupted": "Step 1) ... (error inserted)",
  "first_error": "Step 2"
}
```

notes:image_url: external link to the image (not hosted in this repo). Users should download/copy the images locally.Some URLs may expire; please handle missing downloads gracefully.



## ⚡ Quick Start
1. Clone the repository
   
2. Download images
We provide a helper script to cache images locally:
```
python data/download_images.py \
  --input data/download_images_url.jsonl \
  --output-dir data/images/
```

3. Run inference
   
We provide system prompt and format of output in inference/example_inference.py

## 📄 License

This project is distributed under the terms of the [LICENSE](./LICENSE).
