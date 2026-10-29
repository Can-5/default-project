#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""devops — Dağıtım/altyapı ajanı (5-ajon toolkit'ten biri)."""

import os
from datetime import datetime
from pathlib import Path


def analyze(target):
    findings = []
    target = Path(target)
    files = [p.name for p in target.iterdir()] if target.is_dir() else []

    ci_files = [f for f in files if f.startswith(".github/") or f.startswith(".gitlab/") or f.startswith(".circleci/")]
    docker_files = [f for f in files if f.lower() in ("dockerfile", "docker-compose.yml", "docker-compose.yaml")]
    req_files = [f for f in files if f.lower() in ("requirements.txt", "pyproject.toml", "setup.py", "poetry.lock")]

    if not ci_files:
        findings.append({
            "file": str(target), "line": 0, "severity": "medium",
            "type": "devops", "message": "CI/CD yapılandırma dosyası eksik",
        })
    if not docker_files:
        findings.append({
            "file": str(target), "line": 0, "severity": "low",
            "type": "devops", "message": "Docker dosyası eksik (konteynerlaştırma önerilir)",
        })
    if not req_files:
        findings.append({
            "file": str(target), "line": 0, "severity": "high",
            "type": "devops", "message": "Bağımlılık dosyası eksik (requirements.txt/pyproject.toml)",
        })

    return {
        "agent": "devops",
        "target": str(target),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(files),
        "findings": findings,
    }