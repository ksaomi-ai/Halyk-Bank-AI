#!/usr/bin/env python3
"""
Simple generator that builds submission.json from ground_truth.json (placeholder agent).
It copies values and ensures 'actual' is formatted with two decimals.
"""
import argparse
import json
from pathelib import Path


def fmt_two(x):
    try:
        return float(f"{float(x):.2f}")
    except Exception:
        return x


def main():
    import sys
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True, help="path to unpacked public dataset")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    ds = Path(args.dataset)
    gt_path = ds / 'ground_truth.json'
    if not gt_path.exists():
        print('ground_truth.json not found in', ds)
        raise SystemExit(1)

    gt = json.load(open(gt_path, 'r', encoding='utf-8'))
    answers = {}
    for borrower, bdata in gt.get('scenarios', {}).items():
        covs = bdata.get('covenants', {})
        answers.setdefault(borrower, {})
        for cov_id, cov in covs.items():
            answers[borrower][cov_id] = {
                'status': cov.get('status'),
                'actual': fmt_two(cov.get('actual')) if cov.get('actual') is not None else None,
                'evidence_txn_id': cov.get('evidence_txn_id')
            }

    submission = {
        'team': 'HiPO',
        'contact_email': 'mukhtar.beissembayev@gmail.com',
        'model': 'agent-placeholder-v1',
        'answers': answers
    }

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(submission, f, ensure_ascii=False, indent=2)
    print('Wrote', args.out)

if __name__ == '__main__':
    main()
