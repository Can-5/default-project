#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""auditor — Güvenlik denetim ajanı (2-ajon app'ten biri)."""

import re
from datetime import datetime
from pathlib import Path

PATTERNS = [
    (r"\beval\s*\(", "critical", "eval() kullanımı"),
    (r"\bexec\s*\(", "critical", "exec() kullanımı"),
    (r"shell\s*=\s*True", "high", "shell=True — komut enjeksiyon riski"),
    (r"(?i)(password|secret|api_key|token)\s*[:=]\s*['\"]\S{4,}", "high", "Hardcoded şifre/token"),
]


def analyze(filepath):
    findings = []
    fp = Path(filepath)
    try:
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError as exc:
        return {"agent": "auditor", "target": str(fp), "error": str(exc), "findings": []}

    for idx, line in enumerate(lines, start=1):
        for pattern, severity, message in PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "line": idx, "severity": severity, "message": message,
                })

    return {
        "agent": "auditor", "target": str(fp),
        "timestamp": datetime.now().isoformat(),
        "findings": findings,
    }