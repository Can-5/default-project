#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""security — Güvenlik denetim ajanı (5-ajon toolkit'ten biri)."""

import os
import re
from datetime import datetime
from pathlib import Path

PATTERNS = [
    (r"\beval\s*\(", "critical", "eval() kullanımı — kod enjeksiyon riski"),
    (r"\bexec\s*\(", "critical", "exec() kullanımı — kod enjeksiyon riski"),
    (r"shell\s*=\s*True", "high", "shell=True — komut enjeksiyon riski"),
    (r"(?i)(password|secret|api_key|token)\s*[:=]\s*['\"]\S{4,}", "high", "Hardcoded şifre/token"),
    (r"(?i)(sk-|AKIA[0-9A-Z]{16})", "critical", "API anahtarı desenine uygun hardcoded değer"),
    (r"\.innerHTML\s*=", "medium", "innerHTML — XSS riski"),
    (r"pickle\.loads\s*\(", "high", "pickle.loads — güvenli olmayan seri durumlandırma"),
]


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
            for pattern, severity, message in PATTERNS:
                if re.search(pattern, line):
                    findings.append({
                        "file": str(fp), "line": idx, "severity": severity,
                        "type": "security", "message": message,
                    })

    return {
        "agent": "security",
        "target": str(target),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(files),
        "findings": findings,
    }