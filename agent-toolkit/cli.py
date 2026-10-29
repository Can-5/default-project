#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli — agent-toolkit komut satırı arayüzü."""

import json
import sys

from dispatcher import Dispatcher
from aggregator import Aggregator


def main():
    import argparse
    parser = argparse.ArgumentParser(description="5 ajanın kullanabileceği modüler yazılım CLI")
    parser.add_argument("--target", required=True, help="Hedef dosya veya klasör yolu")
    parser.add_argument("--run", required=True, help="Ajan adı (reviewer/security/debugger/researcher/devops) veya 'all'")
    parser.add_argument("--json", action="store_true", help="JSON çıkış")
    parser.add_argument("--out", default="reports", help="Rapor dizini")
    args = parser.parse_args()

    disp = Dispatcher(args.target)

    if args.run == "all":
        results = disp.run_all()
        disp.save(results, args.out)
        if args.json:
            print(Aggregator(results).to_json())
        else:
            print(Aggregator(results).build_report())
    else:
        res = disp.run(args.run)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"[cli] Ajan: {res['agent']} | dosya: {res['files_scanned']} | bulgu: {len(res['findings'])}")
            for f in res["findings"]:
                print(f"  [{f.get('severity','?')}] {f['file']}:{f['line']} — {f['message']}")


if __name__ == "__main__":
    main()