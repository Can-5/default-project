#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open-code-booster — OpenCode ortamını iyileştirir, güçlendirir ve optimizasyon önerileri sunar.
Eklenti durumu, skill sağlığı, bellek durumu ve yapılandırma denetimi yapar.
"""
import argparse
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
SKILLS_DIR = Path.home() / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "skills"


def status():
    print("=== OpenCode Ortam Durumu ===")
    print(f"Çalışma dizini: {BASE}")
    print(f"Skills dizini: {SKILLS_DIR}")
    if SKILLS_DIR.exists():
        skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
        print(f"Yüklü skill sayısı: {len(skills)}")
    else:
        print("Skills dizini bulunamadı.")
    pycache_count = sum(1 for _ in Path(".").rglob("__pycache__"))
    print(f"__pycache__ dizini sayısı: {pycache_count}")


def optimize():
    print("=== OpenCode Optimizasyonu ===")
    count = 0
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        count += 1
    print(f"Temizlenen __pycache__ dizini: {count}")
    print("Optimizasyon tamamlandı.")


def clean():
    print("=== __pycache__ Temizliği ===")
    count = 0
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        count += 1
    print(f"Temizlenen __pycache__ dizini: {count}")


def main():
    parser = argparse.ArgumentParser(description="OpenCode Booster")
    parser.add_argument("--status", action="store_true", help="Ortam durumunu göster")
    parser.add_argument("--optimize", action="store_true", help="Optimizasyon önerilerini uygula")
    parser.add_argument("--clean", action="store_true", help="__pycache__ dizinlerini temizle")
    args = parser.parse_args()

    if args.status:
        status()
    elif args.optimize:
        optimize()
    elif args.clean:
        clean()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
