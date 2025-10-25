#!/usr/bin/env python3
"""
Evaluation script for First Error Detection.

This script calculates the accuracy of a model's ability to identify the first incorrect step in a reasoning process.
It compares the model's predictions against the ground truth labels from the benchmark file.

The script supports various model output formats and provides both overall accuracy and
accuracy broken down by corruption type.

Usage:
    python evaluation/eval_first_error.py \
        --prediction_file <path_to_model_predictions.jsonl> \
        --benchmark_file <path_to_benchmark.jsonl>
"""

import json
import os
import re
import argparse
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict

# --- Prediction Extraction Logic ---

def extract_prediction_from_glm_thinking(prediction_text: str) -> str:
    """Extract prediction from GLM thinking format."""
    answer_match = re.search(r'<answer>(.*?)</answer>', prediction_text, re.DOTALL)
    if answer_match:
        content = answer_match.group(1).strip()
        box_match = re.search(r'<\|begin_of_box\|>(.*?)<\|end_of_box\|>', content, re.DOTALL)
        return box_match.group(1).strip() if box_match else content
    box_match = re.search(r'<\|begin_of_box\|>(.*?)<\|end_of_box\|>', prediction_text, re.DOTALL)
    return box_match.group(1).strip() if box_match else prediction_text.strip()

def extract_prediction_from_internvl(prediction_text: str) -> str:
    """Extract prediction from InternVL format."""
    match = re.search(r'(?:Final Answer:|Answer:)\s*([^\n]+)', prediction_text, re.IGNORECASE)
    if match:
        return re.sub(r'\*+', '', match.group(1)).strip()
    lines = prediction_text.strip().split('\n')
    for line in reversed(lines):
        if ':' in line and len(line.split(':', 1)[1].strip()) > 0:
            return line.split(':', 1)[1].strip()
    return prediction_text.strip()

def extract_prediction_from_idefics2(prediction_text: str) -> str:
    """Extract prediction from Idefics2 format."""
    match = re.search(r'Assistant:\s*(.+?)(?:\n|$)', prediction_text, re.DOTALL)
    if match:
        return re.sub(r'[.!?]+$', '', match.group(1)).strip()
    return prediction_text.strip()

def extract_prediction_from_minicpm(prediction_text: str) -> str:
    """Extract prediction from MiniCPM format."""
    prediction = prediction_text.strip()
    prediction = re.sub(r'^(Answer:|The answer is:?|Response:)\s*', '', prediction, flags=re.IGNORECASE)
    return re.sub(r'[.!?]+$', '', prediction).strip()

def extract_model_prediction(entry: Dict[str, Any], model_name: Optional[str] = None) -> str:
    """
    Extract prediction from a model's output entry.
    This function is designed to be robust to various output formats.
    """
    # --- Start of format-specific extraction logic ---
    
    # Handle GLM-like formats with <think> and <answer> tags
    if "prediction" in entry and isinstance(entry["prediction"], str) and "<think>" in entry["prediction"]:
        return extract_prediction_from_glm_thinking(entry["prediction"])

    # Handle formats where the prediction is in a specific, known key
    # This part can be customized based on the models you evaluate.
    # Example:
    # if 'gpt4o_prediction' in entry:
    #     return str(entry['gpt4o_prediction']).strip()
    # if 'MMada_answer' in entry:
    #     return str(entry['MMada_answer']).strip()

    # --- Fallback to more general patterns ---

    # Look for a key named "prediction" or "answer"
    for key in ["prediction", "answer"]:
        if key in entry and entry[key] is not None:
            value = entry[key]
            # Apply specific extractors if content matches a known complex format
            if isinstance(value, str):
                if "Assistant:" in value:
                    return extract_prediction_from_idefics2(value)
                if "Final Answer:" in value:
                    return extract_prediction_from_internvl(value)
            return str(value).strip()

    # Look for any key containing "prediction" (e.g., "model_prediction")
    for key, value in entry.items():
        if "prediction" in key.lower() and value is not None:
            return str(value).strip()

    # If no prediction is found, raise an error
    raise ValueError(f"Could not find a valid prediction field in entry with keys: {list(entry.keys())}")

# --- Core Evaluation Logic ---

def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """Loads a JSONL file into a list of dictionaries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def calculate_fe_accuracy(predictions: List[Dict[str, Any]], benchmark: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates first error detection accuracy.
    """
    benchmark_map = {item['id']: item for item in benchmark}
    
    correct_count = 0
    total_count = 0
    missing_predictions = 0
    
    per_corruption_correct = defaultdict(int)
    per_corruption_total = defaultdict(int)
    
    mismatches = []

    for pred_entry in predictions:
        entry_id = pred_entry.get('id')
        if entry_id is None or entry_id not in benchmark_map:
            continue

        total_count += 1
        bench_entry = benchmark_map[entry_id]
        
        ground_truth = bench_entry.get('first_error') or bench_entry.get('correct_step_label')
        corruption_type = bench_entry.get('corruption_type', 'unknown')

        if ground_truth is None:
            continue # Cannot evaluate if ground truth is missing

        per_corruption_total[corruption_type] += 1

        try:
            prediction = extract_model_prediction(pred_entry)
        except ValueError:
            missing_predictions += 1
            continue

        if str(prediction).strip() == str(ground_truth).strip():
            correct_count += 1
            per_corruption_correct[corruption_type] += 1
        else:
            if len(mismatches) < 10: # Log a few examples of mismatches
                mismatches.append({
                    "id": entry_id,
                    "predicted": prediction,
                    "expected": ground_truth,
                    "corruption_type": corruption_type
                })

    # Calculate accuracies
    overall_accuracy = (correct_count / (total_count - missing_predictions)) if (total_count - missing_predictions) > 0 else 0
    
    per_corruption_accuracy = {
        c_type: (per_corruption_correct[c_type] / per_corruption_total[c_type]) if per_corruption_total[c_type] > 0 else 0
        for c_type in per_corruption_total
    }

    return {
        "overall_accuracy": overall_accuracy,
        "correct_predictions": correct_count,
        "valid_predictions": total_count - missing_predictions,
        "total_benchmark_entries": len(benchmark),
        "processed_predictions": total_count,
        "missing_predictions": missing_predictions,
        "per_corruption_accuracy": per_corruption_accuracy,
        "mismatches_sample": mismatches
    }

def main():
    """Main function to run the evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate First Error Detection Accuracy.")
    parser.add_argument("--prediction_file", type=str, required=True, help="Path to the model's prediction JSONL file.")
    parser.add_argument("--benchmark_file", type=str, required=True, help="Path to the benchmark JSONL file.")
    args = parser.parse_args()

    if not os.path.exists(args.prediction_file):
        print(f"Error: Prediction file not found at {args.prediction_file}")
        return
    if not os.path.exists(args.benchmark_file):
        print(f"Error: Benchmark file not found at {args.benchmark_file}")
        return

    print(f"Loading predictions from: {args.prediction_file}")
    predictions = load_jsonl(args.prediction_file)
    
    print(f"Loading benchmark data from: {args.benchmark_file}")
    benchmark = load_jsonl(args.benchmark_file)

    print("\nCalculating First Error Detection Accuracy...")
    results = calculate_fe_accuracy(predictions, benchmark)

    # --- Display Results ---
    print("\n--- Evaluation Results ---")
    print(f"Overall Accuracy: {results['overall_accuracy']:.4f} ({results['correct_predictions']}/{results['valid_predictions']})")
    print(f"Processed Predictions: {results['processed_predictions']}/{len(predictions)}")
    if results['missing_predictions'] > 0:
        missing_pct = (results['missing_predictions'] / results['processed_predictions']) * 100
        print(f"Missing/Failed Predictions: {results['missing_predictions']} ({missing_pct:.1f}%)")
    
    print("\n--- Accuracy by Corruption Type ---")
    if results['per_corruption_accuracy']:
        for c_type, acc in sorted(results['per_corruption_accuracy'].items()):
            print(f"- {c_type:<25}: {acc:.4f}")
    else:
        print("No corruption type data found in the benchmark file.")

    if results['mismatches_sample']:
        print("\n--- Sample of Mismatched Predictions ---")
        for item in results['mismatches_sample']:
            print(f"  ID {item['id']} (Type: {item['corruption_type']}):")
            print(f"    - Predicted: '{item['predicted']}'")
            print(f"    - Expected:  '{item['expected']}'")
    
    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()
