<!-- Top-centered logo -->
<p align="center">
  <a href="https://github.com/JornyWan/PRISM-Bench">
    <img src="assets/prism_logo.png" alt="PRISM-Bench" width="420">
  </a>
</p>

# PRISM-Bench

This repository contains the code and data for **PRISM-Bench**, a benchmark designed to evaluate multimodal large language models (MLLMs) on **reasoning with complex visual puzzles**.

> **🎉 Update (March 2026): PRISM-Bench Data Fully Rereleased!** > Following a rigorous manual review and multiple rounds of auditing, we have resolved the previous data pipeline and CoT hallucination issues. The entire benchmark has been updated and is now fully available. We deeply appreciate the community's feedback, which has been instrumental in making PRISM-Bench more robust.  
> 
> *For full transparency regarding our recent data quality improvements and bug fixes, please see our [Detailed Release Notes & Incident Archive](./Release_Notes_v2.md).*

---
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
