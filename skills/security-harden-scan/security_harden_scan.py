#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security-harden-scan — Kod güvenliği taraması ve sertleştirme.

eval/exec, hardcoded secret, shell=True, subprocess, SQL injection, XSS ve
path traversal kalıplarını tarar.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# (pattern, severity, description, fix_suggestion)
PATTERNS = [
    (r"\beval\s*\(", "critical", "eval() kullanımı — kod enjeksiyon riski", "eval() kullanımını kaldırın; güvenli ayrıştırıcı (ast.literal_eval vb.) kullanın"),
    (r"\bexec\s*\(", "critical", "exec() kullanımı — kod enjeksiyon riski", "exec() kullanımını kaldırın"),
    (r"\bcompile\s*\(", "high", "compile() kullanımı — dinamik kod derleme riski", "compile() kullanımından kaçının"),
    (r"shell\s*=\s*True", "high", "shell=True ile subprocess — komut enjeksiyon riski", "shell=False kullanın ve argüman listesini iletin"),
    (r"\bsubprocess\.", "medium", "subprocess kullanımı — komut çalıştırma riski", "Girdi doğrulamasını ekleyin, shell=False kullanın"),
    (r"(?i)(password|passwd|secret|api_key|token)\s*[:=]\s*['\"]\S{4,}", "high", "Hardcoded şifre/token/secret tespit edildi", "Değeri ortam değişkeninden veya secret store'dan alın"),
    (r"(?i)(sk-|AKIA[0-9A-Z]{16})", "critical", "API anahtarı/token desenine uygun hardcoded değer", "Şifreyi depodan kaldırın, .env veya secret management kullanın"),
    (r"(%\s*\(|f\".*SELECT|f\'.*SELECT)", "medium", "SQL injection riskli sorgu kalıbı", "Parametreli sorgu (prepared statement) kullanın"),
    (r"\.innerHTML\s*=", "medium", "innerHTML ataması — XSS riski", "textContent veya güvenli DOM yöntemi kullanın"),
    (r"\bdocument\.write\s*\(", "medium", "document.write — XSS riski", "document.write yerine güvenli DOM manipulation kullanın"),
    (r"\.\.\/", "low", "Path traversal deseninde '..' kullanımı", "Girdi doğrulayın, os.path.join ve gerçek yol kontrolü yapın"),
    (r"pickle\.loads\s*\(", "high", "pickle.loads — güvenli olmayan seri durumlandırma", "JSON veya güvenli serileştirme formatı kullanın"),
    (r"yaml\.load\s*\(", "medium", "yaml.load — güvenli olmayan YAML yükleme", "yaml.safe_load kullanın"),
]

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEVERITY_LABEL = {
    "critical": "[!CRITICAL]",
    "high": "[!HIGH]",
    "medium": "[!MEDIUM]",
    "low": "[!LOW]",
}


def find_files(path):
    """Verilen yoldaki .py dosyalarını döndürür."""
    p = Path(path)
    if p.is_file():
        return [p] if p.suffix == ".py" else []
    if p.is_dir():
        return sorted(p.rglob("*.py"))
    return []


def scan_file(filepath):
    """Tek bir dosyayı tarar ve bulguları döndürür."""
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError as exc:
        return [{"file": str(filepath), "line": 0, "severity": "critical",
                 "message": f"Dosya okunamadı: {exc}", "fix": ""}]

    for idx, line in enumerate(lines, start=1):
        for pattern, severity, message, fix in PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "file": str(filepath),
                    "line": idx,
                    "severity": severity,
                    "message": message,
                    "fix": fix,
                    "snippet": line.strip(),
                })
    return findings


def scan_path(path, only=None):
    """Verilen yoldaki tüm .py dosyalarını tarar."""
    all_findings = []
    for filepath in find_files(path):
        all_findings.extend(scan_file(filepath))

    if only:
        all_findings = [f for f in all_findings if f["severity"] == only]

    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9),
                                     f["file"], f["line"]))
    return all_findings


def print_findings(findings, json_output=False):
    if json_output:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return

    print(f"[security-harden-scan] Tarama tamamlandı. Toplam bulgu: {len(findings)}")
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    print("Özet: " + ", ".join(f"{k}: {v}" for k, v in counts.items() if v))
    print()

    for f in findings:
        label = SEVERITY_LABEL.get(f["severity"], "[!]")
        print(f"{label} {f['file']}:{f['line']} — {f['message']}")
        print(f"       Kod: {f['snippet']}")
        print(f"       Düzeltme: {f['fix']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Kod güvenliği taraması ve sertleştirme")
    parser.add_argument("--path", required=True, help="Taranacak dosya veya klasör yolu")
    parser.add_argument("--json", action="store_true", help="Çıkışı JSON olarak ver")
    parser.add_argument("--only", choices=list(SEVERITY_ORDER.keys()),
                        help="Sadece belirtilen severity'yi göster")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Hata: yol bulunamadı: {args.path}", file=sys.stderr)
        sys.exit(1)

    findings = scan_path(args.path, only=args.only)
    print_findings(findings, json_output=args.json)


if __name__ == "__main__":
    main()