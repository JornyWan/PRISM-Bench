<!-- Top-centered logo -->
<p align="center">
  <a href="https://github.com/JornyWan/PRISM-Bench">
    <img src="assets/prism_logo.png" alt="PRISM-Bench" width="420">
  </a>
</p>

# PRISM-Bench

<p align="center">
  <a href="https://arxiv.org/abs/2510.23594"><strong>📄 Paper</strong></a> •
  <a href="https://jornywan.github.io/PRISM-Bench-web/"><strong>🌐 Website</strong></a>
</p>

This repository contains the code and data for **PRISM-Bench**, a benchmark designed to evaluate multimodal large language models (MLLMs) on **reasoning with complex visual puzzle**.

---

## 🚀 Features

- **Diverse Visual Reasoning Tasks**: puzzles, graph-based reasoning, pattern recognition, algorithmic reasoning, etc.  
- **Chain-of-Thought (CoT) Annotations**: ground-truth reasoning steps for each problem.
- **Instruction Corruption**: synthetic corrupted reasoning chains for robustness testing.  
- **First-Error Detection**: annotations for the first mistake in incorrect reasoning chains.   
- **VQA-Style Evaluation**: multiple-choice format with definitive ground-truth answers.  

---

## 📂 Repository Structure

```
├── data/
│ ├── PRISM-Bench.json # Main benchmark file (with image URLs, Q/A, reasoning, etc.)
│ ├── download_images_url.jsonl #jsonl file for downloading images
│ ├── download_images.py #Script to download images from url
│ └── example/ # Small demo subset
├── inference/
│ └── example_inference.py # Example inference scripts
├── evaluation/
│ ├── eval_vqa.py # Accuracy evaluation
│ └── eval_first_error.py # First-error detection evaluation
│ └── README.md # Evaluation Guideline
└── README.md
```

---

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

4. Run evaluation
   
We provide evaluation code in evaluation/eval_first_error.py and evaluation/eval_vqa.py,
for details, please read the instructions at evaluation/README.md

## 📈 Evaluation Metrics

First-Error Detection: whether the model correctly identifies the first incorrect reasoning step.

VQA Evaluation: alignment with ground-truth answers in a multiple-choice setting.

## 📄 License

This project is distributed under the terms of the [LICENSE](./LICENSE).
