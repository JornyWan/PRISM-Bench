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

We’d like to respond to some of the questions about PRISM-Bench.

First, thank you again to everyone who has taken the time to read the paper and look closely at the benchmark. Regarding the points that were raised:

1. For data quality, we did manually inspect the injected errors themselves (since that is the more challenging part of the task), but we did not carefully audit the step-by-step CoT that was produced when we converted the ground-truth solution into a multi-step reasoning trace using GPT. In that conversion stage, GPT hallucinated in some cases, which led to incorrect step labels. Because this looked like a “simple” text-only transformation step, we did not scrutinize GPT’s outputs as closely as we should have. That is our mistake. We are now systematically checking the generated CoTs, fixing the issues, and will re-release the benchmark once the corrections are complete.

2. Regarding the inference code, the original example_inference script used a dummy image input for the GPT model example. In the appendix of the paper we did show GPT outputs where the model clearly had access to the image, and we later fixed the dummy code after it was pointed out in an issue. We also apologize for having closed that issue too quickly earlier; we reopened it and responded to the new concerns, and in the future we will keep issues open until all questions are fully resolved.

3. On criticism and community discussion, we genuinely appreciate critical feedback and corrections, and we hope discussions can stay friendly and constructive. Our goal and the purpose of this benchmark are to help push forward research on multimodal reasoning. There were oversights in our data pipeline that should not have happened, but each of us is working on this project in our spare time out of genuine interest in the topic, and we’ve invested a lot of time and effort to move this small direction forward.

We’ll take this experience seriously, learn from it, and do better going forward.

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
