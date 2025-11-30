# -*- coding: utf-8 -*-
"""
run_inference.py
Run GPT‑4o inference on benchmark examples to identify incorrect reasoning steps.
Usage:
    python example_inference.py --input benchmark.jsonl --output results.jsonl --image_root path/to/images
"""
import json
import textwrap
import argparse
import base64
import mimetypes
import os
from typing import Dict
import openai
from tqdm import tqdm

# ──────────────────────────────────────────────────────────────────
# 1) SYSTEM PROMPT                                                   │
# ──────────────────────────────────────────────────────────────────
INFERENCE_SYSTEM_PROMPT = textwrap.dedent("""\
You are an expert in logical consistency checking.
You are given:
  - A visual reasoning question,
  - A step-by-step chain-of-thought reasoning to justify the answer,
  - A list of step labels (e.g., "Step 1", ..., "Step n", "None of the steps are incorrect").

Your task is to determine:
  → At which step the reasoning first becomes flawed, if any.
  → If all reasoning is valid, return: "None of the steps are incorrect".

Return exactly one of the step labels as your final answer.
Do not explain your answer.
""")

# ──────────────────────────────────────────────────────────────────
# 2) IMAGE ENCODING                                                  │
# ──────────────────────────────────────────────────────────────────
def encode_image(path: str) -> Dict:
    """Encode image file to base64 and return as dict with url and detail."""
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return {"url": f"data:{mime_type};base64,{encoded}", "detail": "auto"}

# ──────────────────────────────────────────────────────────────────
# 3) GPT CALL                                                        │
# ──────────────────────────────────────────────────────────────────
def run_inference_on_entry(entry: Dict, image_root: str, model: str = "gpt-4o") -> str:
    client = openai.Client(api_key="")  # your key
    
    step_options = entry["step_options"]
    reasoning = entry["corrupted_cot"]
    
    # Build full image path and encode
    image_path = os.path.join(image_root, entry["image"])
    image_input = encode_image(image_path)
    
    # Construct user prompt with both text and image
    user_prompt = [
        {
            "type": "text",
            "text": textwrap.dedent(f"""\
                Question: {entry['question_text']}
                
                Step-by-step reasoning:
                {reasoning}
                
                Step options:
                {step_options}
                """)
        },
        {
            "type": "image_url",
            "image_url": image_input
        }
    ]
    
    rsp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": INFERENCE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    prediction = rsp.choices[0].message.content.strip()
    return prediction

# ──────────────────────────────────────────────────────────────────
# 4) MAIN SCRIPT                                                     │
# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True,
                        help="Path to benchmark .jsonl file")
    parser.add_argument("--output", type=str, required=True,
                        help="Path to save results .jsonl")
    parser.add_argument("--image_root", type=str, required=True,
                        help="Folder containing image files")
    parser.add_argument("--model", type=str, default="gpt-4o",
                        help="Model name (default: gpt-4o)")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    print(f"[INFO] Running inference on {len(lines)} examples...")

    out_file = open(args.output, "w", encoding="utf-8")
    for i, entry in enumerate(tqdm(lines, desc="GPT-4o inference")):
        try:
            prediction = run_inference_on_entry(entry, args.image_root, model=args.model)
            entry["gpt4o_prediction"] = prediction
        except Exception as e:
            entry["gpt4o_prediction"] = f"[ERROR] {e}"

        out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    out_file.close()
    print(f"[✓] Inference complete. Results saved to {args.output}")
