#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reviewer — Kod kalitesi inceleme ajanı (2-ajon app'ten biri)."""

import ast
import re
from datetime import datetime
from pathlib import Path


def analyze(filepath):
    findings = []
    fp = Path(filepath)
    try:
        src = fp.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return {"agent": "reviewer", "target": str(fp), "error": str(exc), "findings": []}

    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {
            "agent": "reviewer", "target": str(fp),
            "timestamp": datetime.now().isoformat(),
            "findings": [{"line": 0, "severity": "high", "message": "Söz dizimi hatası"}],
        }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and len(node.args.args) > 5:
            findings.append({
                "line": node.lineno, "severity": "medium",
                "message": f"Fonksiyon '{node.name}' çok fazla parametre",
            })

    for idx, line in enumerate(src.splitlines(), start=1):
        if re.search(r"\bTODO\b|\bFIXME\b", line):
            findings.append({
                "line": idx, "severity": "low", "message": "TODO/FIXME yorumu",
            })

    return {
        "agent": "reviewer", "target": str(fp),
        "timestamp": datetime.now().isoformat(),
        "findings": findings,
    }