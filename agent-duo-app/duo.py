#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""duo — 2 ajanı (reviewer + auditor) çalıştıran ve sonuçları birleştiren."""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents.reviewer import analyze as review_analyze
from agents.auditor import analyze as audit_analyze


def run_duo(filepath):
    review = review_analyze(filepath)
    audit = audit_analyze(filepath)

    total = len(review.get("findings", [])) + len(audit.get("findings", []))
    report = {
        "target": str(Path(filepath).resolve()),
        "timestamp": datetime.now().isoformat(),
        "agents": ["reviewer", "auditor"],
        "review": review,
        "audit": audit,
        "total_findings": total,
    }
    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="2-ajon duo uygulama")
    parser.add_argument("--target", required=True, help="Hedef dosya yolu")
    parser.add_argument("--json", action="store_true", help="JSON çıkış")
    parser.add_argument("--out", default="reports", help="Rapor dizini")
    args = parser.parse_args()

    report = run_duo(args.target)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = out / f"duo_{stamp}.json"
    fn.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"[duo-app] Hedef: {report['target']}")
        print(f"[duo-app] Toplam bulgu: {report['total_findings']}")
        print(f"  reviewer: {len(report['review'].get('findings', []))}")
        print(f"  auditor: {len(report['audit'].get('findings', []))}")
        print(f"[duo-app] Rapor: {fn}")


if __name__ == "__main__":
    main()