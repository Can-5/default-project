#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debugger — Hata ayıklama ajanı (5-ajon toolkit'ten biri)."""

import re
from datetime import datetime
from pathlib import Path


def analyze(target):
    findings = []
    target = Path(target)
    files = []
    if target.is_file():
        files = [target] if target.suffix == ".py" else []
    elif target.is_dir():
        files = sorted(target.rglob("*.py"))

    for fp in files:
        try:
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            if re.search(r"\bprint\s*\(", line):
                findings.append({
                    "file": str(fp), "line": idx, "severity": "low",
                    "type": "debug", "message": "print() ifadesi bulundu (debug kodu olabilir)",
                })
            if re.search(r"except\s*:", line):
                findings.append({
                    "file": str(fp), "line": idx, "severity": "medium",
                    "type": "debug", "message": "Boş except bloğu (hata yakalama yoksayıyor)",
                })
            if re.search(r"\b(pdb|breakpoint)\s*\(", line):
                findings.append({
                    "file": str(fp), "line": idx, "severity": "medium",
                    "type": "debug", "message": "pdb/breakpoint kaldırılmamış",
                })

    return {
        "agent": "debugger",
        "target": str(target),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(files),
        "findings": findings,
    }