#!/usr/bin/env python3
"""
Evaluation script for Visual Question Answering (VQA) accuracy.

This script calculates the VQA accuracy by comparing the model's predicted answer
to the ground truth answer in the benchmark file.

The script is designed to handle various model output formats where the VQA answer
might be stored.

Usage:
    python evaluation/eval_vqa.py \
        --prediction_file <path_to_model_predictions.jsonl> \
        --benchmark_file <path_to_benchmark.jsonl>
"""

import json
import os
import re
import argparse
from typing import Dict, List, Any, Optional
from collections import defaultdict

# --- Prediction Extraction Logic ---

def extract_vqa_answer(entry: Dict[str, Any]) -> Optional[str]:
    """
    Extracts the VQA answer from a model's output entry.
    It checks for common keys where the VQA answer might be stored.
    """
    # Check for a specific key first, e.g., 'vqa_answer'
    if 'vqa_answer' in entry and entry['vqa_answer'] is not None:
        return str(entry['vqa_answer']).strip()

    # Fallback to check other possible keys like 'vqa_prediction' or 'answer'
    for key in ['vqa_prediction', 'answer']:
        if key in entry and entry[key] is not None:
            return str(entry[key]).strip()
            
    # A more general check for any key containing 'vqa' and 'answer'
    for key, value in entry.items():
        if 'vqa' in key.lower() and 'answer' in key.lower() and value is not None:
            return str(value).strip()

    # If no specific VQA answer is found, return None
    return None

# --- Core Evaluation Logic ---

def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """Loads a JSONL file into a list of dictionaries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def calculate_vqa_accuracy(predictions: List[Dict[str, Any]], benchmark: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates VQA accuracy.
    """
    benchmark_map = {item['id']: item for item in benchmark}
    
    correct_count = 0
    total_count = 0
    missing_answers = 0
    
    mismatches = []

    for pred_entry in predictions:
        entry_id = pred_entry.get('id')
        if entry_id is None or entry_id not in benchmark_map:
            continue

        total_count += 1
        bench_entry = benchmark_map[entry_id]
        
        ground_truth = bench_entry.get('vqa_answer')

        if ground_truth is None:
            continue # Cannot evaluate if ground truth is missing

        predicted_answer = extract_vqa_answer(pred_entry)

        if predicted_answer is None:
            missing_answers += 1
            continue

        # Simple exact match for VQA evaluation
        if predicted_answer.lower().strip() == str(ground_truth).lower().strip():
            correct_count += 1
        else:
            if len(mismatches) < 10: # Log a few examples of mismatches
                mismatches.append({
                    "id": entry_id,
                    "predicted": predicted_answer,
                    "expected": ground_truth
                })

    # Calculate accuracy
    valid_predictions = total_count - missing_answers
    overall_accuracy = (correct_count / valid_predictions) if valid_predictions > 0 else 0

    return {
        "overall_accuracy": overall_accuracy,
        "correct_predictions": correct_count,
        "valid_predictions": valid_predictions,
        "total_benchmark_entries": len(benchmark),
        "processed_predictions": total_count,
        "missing_answers": missing_answers,
        "mismatches_sample": mismatches
    }

def main():
    """Main function to run the VQA evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate Visual Question Answering (VQA) Accuracy.")
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

    print("\nCalculating VQA Accuracy...")
    results = calculate_vqa_accuracy(predictions, benchmark)

    # --- Display Results ---
    print("\n--- VQA Evaluation Results ---")
    print(f"Overall Accuracy: {results['overall_accuracy']:.4f} ({results['correct_predictions']}/{results['valid_predictions']})")
    print(f"Processed Predictions: {results['processed_predictions']}/{len(predictions)}")
    if results['missing_answers'] > 0:
        missing_pct = (results['missing_answers'] / results['processed_predictions']) * 100
        print(f"Entries with Missing VQA Answers: {results['missing_answers']} ({missing_pct:.1f}%)")

    if results['mismatches_sample']:
        print("\n--- Sample of Mismatched VQA Answers ---")
        for item in results['mismatches_sample']:
            print(f"  ID {item['id']}:")
            print(f"    - Predicted: '{item['predicted']}'")
            print(f"    - Expected:  '{item['expected']}'")
    
    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()
