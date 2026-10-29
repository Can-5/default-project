#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dispatcher — 5 ajanı yönlendiren dağıtıcı."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Paket içinden import etmeyi destekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.reviewer import analyze as review_analyze
from agents.security import analyze as security_analyze
from agents.debugger import analyze as debugger_analyze
from agents.researcher import analyze as researcher_analyze
from agents.devops import analyze as devops_analyze

AGENTS = {
    "reviewer": review_analyze,
    "security": security_analyze,
    "debugger": debugger_analyze,
    "researcher": researcher_analyze,
    "devops": devops_analyze,
}


class Dispatcher:
    def __init__(self, target):
        self.target = target

    def run(self, agent_name):
        if agent_name not in AGENTS:
            raise ValueError(f"Bilinmeyen ajan: {agent_name}. Mevcut: {list(AGENTS)}")
        return AGENTS[agent_name](self.target)

    def run_all(self):
        results = {}
        for name, fn in AGENTS.items():
            results[name] = fn(self.target)
        return results

    def save(self, results, out_dir="reports"):
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved = []
        for name, res in results.items():
            fn = out / f"{name}_{stamp}.json"
            fn.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
            saved.append(str(fn))
        return saved


def main():
    import argparse
    parser = argparse.ArgumentParser(description="5-ajon dispatcher")
    parser.add_argument("--target", required=True, help="Hedef dosya veya klasör")
    parser.add_argument("--run", required=True, help="Ajan adı veya 'all'")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    parser.add_argument("--out", default="reports", help="Rapor dizini")
    args = parser.parse_args()

    disp = Dispatcher(args.target)
    if args.run == "all":
        results = disp.run_all()
        saved = disp.save(results, args.out)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"[dispatcher] 5 ajan çalıştırıldı, {len(saved)} rapor kaydedildi:")
            for s in saved:
                print(f"  {s}")
    else:
        res = disp.run(args.run)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"[dispatcher] Ajan: {res['agent']}, dosya: {res['files_scanned']}, bulgu: {len(res['findings'])}")
            for f in res["findings"]:
                print(f"  [{f.get('severity','?')}] {f['file']}:{f['line']} — {f['message']}")


if __name__ == "__main__":
    main()