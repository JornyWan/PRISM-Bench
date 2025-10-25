# Evaluation Scripts

This directory contains scripts to evaluate model performance on the benchmark.

## 1. First Error Detection

This task evaluates the model's ability to identify the first incorrect step in a multi-step reasoning process.

### Usage

To run the evaluation, use the `eval_first_error.py` script. You need to provide the path to your model's prediction file and the benchmark file.

```bash
python evaluation/eval_first_error.py \
    --prediction_file /path/to/your/model_predictions.jsonl \
    --benchmark_file /path/to/benchmark.jsonl
```

### Input File Formats

-   **Prediction File (`--prediction_file`)**: A JSONL file where each line is a JSON object corresponding to a benchmark item. The script is designed to automatically detect the prediction from various formats, but it primarily looks for a `prediction` or `answer` key. Each JSON object must contain an `id` that matches the `id` in the benchmark file.

    *Example:*
    ```json
    {"id": "unique_id_1", "prediction": "Step 3"}
    {"id": "unique_id_2", "prediction": "Step 1"}
    ```

-   **Benchmark File (`--benchmark_file`)**: The ground truth JSONL file provided with the benchmark. Each line should contain an `id`, the `first_error` label, and the `corruption_type`.

### Output

The script will print the following metrics to the console:

-   **Overall Accuracy**: The percentage of predictions that correctly match the ground truth.
-   **Accuracy by Corruption Type**: A breakdown of accuracy for each type of error introduced in the reasoning steps.
-   **Sample of Mismatches**: A few examples of incorrect predictions to help with error analysis.

---

## 2. Visual Question Answering (VQA)

This task evaluates the model's accuracy on the visual question answering portion of the benchmark.

### Usage

To run the evaluation, use the `eval_vqa.py` script.

```bash
python evaluation/eval_vqa.py \
    --prediction_file /path/to/your/model_predictions.jsonl \
    --benchmark_file /path/to/benchmark.jsonl
```

### Input File Formats

-   **Prediction File (`--prediction_file`)**: A JSONL file where each line is a JSON object. The script looks for a `vqa_answer` or `answer` key to find the model's VQA response. Each object must have an `id`.

    *Example:*
    ```json
    {"id": "unique_id_1", "vqa_answer": "Yes"}
    {"id": "unique_id_2", "vqa_answer": "No"}
    ```

-   **Benchmark File (`--benchmark_file`)**: The ground truth JSONL file, which should contain the `id` and the correct `vqa_answer`.

### Output

The script will report:

-   **Overall VQA Accuracy**: The percentage of VQA answers that are an exact match to the ground truth.
-   **Sample of Mismatches**: Examples of incorrect VQA answers.
