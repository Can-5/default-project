#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""researcher — Araştırma/dökümantasyon ajanı (5-ajon toolkit'ten biri)."""

import re
from datetime import datetime
from pathlib import Path


def analyze(target):
    findings = []
    target = Path(target)
    files = []
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(target.rglob("*"))

    has_readme = any(p.name.lower() == "readme.md" for p in files)
    py_files = [p for p in files if p.suffix == ".py"]

    if not has_readme:
        findings.append({
            "file": str(target), "line": 0, "severity": "medium",
            "type": "documentation", "message": "README.md eksik",
        })

    for fp in py_files:
        try:
            src = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if not src.strip().startswith('"""') and "'''" not in src[:100]:
            findings.append({
                "file": str(fp), "line": 1, "severity": "low",
                "type": "documentation", "message": "Modül/docstring eksik",
            })

    return {
        "agent": "researcher",
        "target": str(target),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(py_files),
        "findings": findings,
    }