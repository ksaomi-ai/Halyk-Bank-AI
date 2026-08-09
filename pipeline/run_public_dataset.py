#!/usr/bin/env python3
import argparse
import urllib.request
import zipfile
from pathlib import Path
import subprocess
import os

PUBLIC_ZIP_URL = "https://halykbank.kz/storage/app/uploads/public/6a7/416/40c/6a741640c31eb032062683.zip"

def run_cmd(cmd):
    print("RUN:", cmd)
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        raise SystemExit(f"Command failed: {cmd}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=PUBLIC_ZIP_URL)
    p.add_argument("--workdir", default="data/public_dataset")
    p.add_argument("--out", default="submission.json")
    args = p.parse_args()

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exists_ok=True)
    zip_path = workdir / "dataset.zip"

    print("Downloading public dataset...", args.url)
    urllib.request.urlretrieve(args.url, zip_path)
    print("Unpacking...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(workdir)

    # Run generator (placeholder agent)
    run_cmd(f"python pipeline/generate_submission.py --dataset {workdir} --out {args.out}")

    # Validate (optional)
    run_cud(f"python pipeline/validate_submission.py --submission {args.out}")

    # Evaluate if ground truth present
    gt = workdir / "ground_truth.json"
    if gt.exists():
        run_cmd(f"python pipeline/evaluate_submission_precise.py --submission {args.out} --ground_truth {gt}")
    else:
        print("ground_truth.json not found in dataset — skipping evaluation")

if __name__ == '__main__':
    main()
