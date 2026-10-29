#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reviewer — Kod kalitesi inceleme ajanı (5-ajon toolkit'ten biri)."""

import ast
import os
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
            src = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = src.splitlines()
        try:
            tree = ast.parse(src)
        except SyntaxError:
            findings.append({
                "file": str(fp), "line": 0, "type": "syntax",
                "severity": "high", "message": "Söz dizimi hatası, dosya parse edilemiyor",
            })
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    findings.append({
                        "file": str(fp), "line": node.lineno, "type": "complexity",
                        "severity": "medium",
                        "message": f"Fonksiyon '{node.name}' çok fazla parametre ({len(node.args.args)})",
                    })
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 10:
                    findings.append({
                        "file": str(fp), "line": node.lineno, "type": "complexity",
                        "severity": "medium",
                        "message": f"Sınıf '{node.name}' çok fazla metot ({len(methods)})",
                    })

        for idx, line in enumerate(lines, start=1):
            if re.search(r"\bTODO\b|\bFIXME\b|\bXXX\b", line):
                findings.append({
                    "file": str(fp), "line": idx, "type": "todo",
                    "severity": "low", "message": "TODO/FIXME/XXX yorumu bulundu",
                })

    return {
        "agent": "reviewer",
        "target": str(target),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(files),
        "findings": findings,
    }