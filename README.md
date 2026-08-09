# Halyk Bank AI — Agentic pipeline

This repository contains a minimal runnable pipeline for the Halyk AI Challenge that downloads the public dataset, generates a submission.json (by reformatting the ground_truth if present) and evaluates it using the official scoring rules (status 0.50, actual 0.30 with linear decay to 0 at 5%, evidence 0.20; when evidence is null, evidence points decay with actual).

This forkable project is intended so anyone can clone, set their own LLM API keys (if they want to extend the agent), and run the pipeline locally or in CI.

Quick start
-----------
1. Clone the repo:
   git clone https://github.com/ksaomi-ai/Halyk-Bank-AI.git
   cd Halyk-Bank-AI
2. Create a Python virtual environment and install dependencies:
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
3. Run the public dataset pipeline (will download the public zip automatically):
   python pipeline/run_public_dataset.py --out submission.json
4. If ground_truth.json is present in the downloaded dataset, evaluation will be run automatically and a report will be saved to runs/eval_report.json.

Notes
-----
- If you want to use a real LLM, put your API keys into a `.env` file (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.) and extend pipeline/run_agent.py to call the model of your choice.
- The included `pipeline/generate_submission.py` is a placeholder that copies ground_truth into submission.json (so you can test the evaluator and workflow). Replace it with your agent implementation.

Files of interest
-----------------
- pipeline/run_public_dataset.py — orchestrator: downloads dataset, runs generation and evaluation
- pipeline/generate_submission.py — placeholder agent: converts ground_truth -> submission
- pipeline/evaluate_submission_precise.py — precise evaluator implementing scoring rules
- submission_template.json — template for answers
- .github/workflows/run_public_dataset.yml — GitHub Actions workflow to run pipeline
- requirements.txt — Python dependencies

License: MIT
