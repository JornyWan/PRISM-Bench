# -*- coding: utf-8 -*-
"""
run_inference.py
Run GPT‑4o inference on benchmark examples to identify incorrect reasoning steps.

Usage:
    python example_inference.py --input benchmark.jsonl --output results.jsonl
"""

import json
import textwrap
import argparse
from typing import Dict
import openai
from tqdm import tqdm

# ────────────────────────────────────────────────────────────────────
# 1) SYSTEM PROMPT                                                   │
# ────────────────────────────────────────────────────────────────────
INFERENCE_SYSTEM_PROMPT = textwrap.dedent("""\
You are an expert in logical consistency checking.

You are given:
- A visual reasoning question,
- A step-by-step chain-of-thought reasoning to justify the answer,
- A list of step labels (e.g., "Step 1", ..., "Step n", "None of the steps are incorrect").

Your task is to determine:
→ At which step the reasoning first becomes flawed, if any.
→ If all reasoning is valid, return: "None of the steps are incorrect".

Return exactly one of the step labels as your final answer. Do not explain your answer.
""")

# ────────────────────────────────────────────────────────────────────
# 2) GPT CALL                                                        │
# ────────────────────────────────────────────────────────────────────
def run_inference_on_entry(entry: Dict,
                            model: str = "o3-2025-04-16") -> str:
    client = openai.Client(api_key="")         # your key
    

    step_options = entry["step_options"]
    reasoning = entry["corrupted_cot"]

    user_prompt = textwrap.dedent(f"""\
    Question: {entry['question_text']}
    Image path: {entry['image']}
    Step-by-step reasoning:
    {reasoning}

    Step options:
    {step_options}
    """)

    rsp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": INFERENCE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    prediction = rsp.choices[0].message.content.strip()
    return prediction

# ────────────────────────────────────────────────────────────────────
# 3) MAIN SCRIPT                                                     │
# ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to benchmark .jsonl file")
    parser.add_argument("--output", type=str, required=True, help="Path to save results .jsonl")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    print(f"[INFO] Running inference on {len(lines)} examples...")
    out_file = open(args.output, "w", encoding="utf-8")

    for i, entry in enumerate(tqdm(lines, desc="GPT-4o inference")):
        try:
            prediction = run_inference_on_entry(entry)
            entry["gpt-o3_prediction"] = prediction
        except Exception as e:
            entry["gpt-o3_prediction"] = f"[ERROR] {e}"

        out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")


    out_file.close()
    print(f"[✓] Inference complete. Results saved to {args.output}")
