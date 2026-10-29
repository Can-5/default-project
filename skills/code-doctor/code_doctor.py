#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code-doctor — Kod analiz, bug tespiti ve iyileştirme önerileri.
Python dosyalarını tarar ve yaygın sorunları raporlar.
"""

import argparse
import ast
import os
import sys
from pathlib import Path


class CodeDoctor(ast.NodeVisitor):
    """AST tabanlı kod analizcisi."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.issues = []

    def visit_Call(self, node):
        # eval() / exec() kullanımı tespiti
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            self.issues.append({
                "line": node.lineno,
                "severity": "yüksek",
                "message": f"{node.func.id()} kullanımı güvenlik riski oluşturabilir.",
            })
        # print() kullanımı (production'da tercih edilmez)
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.issues.append({
                "line": node.lineno,
                "severity": "düşük",
                "message": "print() kullanımı bulundu; logging kullanılması önerilir.",
            })
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # Boş except bloğu
        if node.type is None:
            self.issues.append({
                "line": node.lineno,
                "severity": "orta",
                "message": "Boş except bloğu (bare except) hataları maskeleyebilir.",
            })
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Hardcoded şifre/anahtar tespiti (basit)
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()
                if any(kw in name for kw in ("password", "secret", "api_key", "token")):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        self.issues.append({
                            "line": node.lineno,
                            "severity": "kritik",
                            "message": f"Hardcoded {target.id} değeri tespit edildi.",
                        })
        self.generic_visit(node)


def analyze_file(filepath):
    """Tek bir Python dosyasını analiz eder."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as exc:  # noqa: BLE001
        return {"file": filepath, "error": str(exc), "issues": []}

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as exc:
        return {"file": filepath, "error": f"Sözdizimi hatası: {exc}", "issues": []}

    doctor = CodeDoctor(filepath)
    doctor.visit(tree)
    return {"file": filepath, "error": None, "issues": doctor.issues}


def analyze_directory(directory):
    """Dizindeki tüm .py dosyalarını analiz eder."""
    results = []
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                results.append(analyze_file(fpath))
    return results


def print_report(results, json_out=False):
    """Analiz raporunu yazdırır."""
    if json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    total_issues = 0
    for res in results:
        if res.get("error"):
            print(f"[HATA] {res['file']}: {res['error']}")
            continue
        if not res["issues"]:
            continue
        print(f"\n📄 {res['file']}")
        for issue in res["issues"]:
            sev_icon = {"kritik": "🔴", "yüksek": "🟠", "orta": "🟡", "düşük": "🟢"}.get(
                issue["severity"], "⚪"
            )
            print(f"  {sev_icon} Satır {issue['line']} [{issue['severity']}]: {issue['message']}")
            total_issues += 1

    print(f"\n✅ Toplam tespit edilen sorun: {total_issues}")


def main():
    parser = argparse.ArgumentParser(description="Kod analiz ve bug tespiti")
    parser.add_argument("path", help="Python dosyası veya dizin yolu")
    parser.add_argument("--json", action="store_true", help="Çıkışı JSON olarak ver")
    args = parser.parse_args()

    path = args.path
    if not os.path.exists(path):
        print(f"Hata: '{path}' bulunamadı.")
        sys.exit(1)

    if os.path.isfile(path):
        results = [analyze_file(path)]
    else:
        results = analyze_directory(path)

    print_report(results, json_out=args.json)


if __name__ == "__main__":
    main()
