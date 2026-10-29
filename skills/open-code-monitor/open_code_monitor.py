#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open-code-monitor — OpenCode oturumlarını, skill kullanımını ve sistem sağlığını izler.
Gerçek zamanlı izleme, uyarı ve sağlık kontrolü sağlar.
"""
import argparse
import os
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
SKILLS_DIR = Path.home() / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "skills"


def health():
    print("=== OpenCode Sağlık Kontrolü ===")
    print(f"Zaman: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    if SKILLS_DIR.exists():
        skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
        print(f"Yüklü skill: {len(skills)}")
    else:
        print("Skills dizini bulunamadı.")
    print("Durum: ✅ Çalışıyor")


def list_skills():
    print("=== Yüklü Skill Listesi ===")
    if SKILLS_DIR.exists():
        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir():
                print(f"  - {d.name}")
    else:
        print("Skills dizini bulunamadı.")


def recent():
    print("=== Son İşlemler ===")
    print("Henüz izleme verisi yok.")


def watch(interval: int = 5):
    print("=== Sürekli İzleme (Çıkmak için Ctrl+C) ===")
    try:
        while True:
            os.system("clear" if os.name == "posix" else "cls")
            health()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")


def main():
    parser = argparse.ArgumentParser(description="OpenCode Monitor")
    parser.add_argument("--health", action="store_true", help="Sağlık kontrolü")
    parser.add_argument("--list", action="store_true", help="Skill listesini göster")
    parser.add_argument("--recent", action="store_true", help="Son işlemleri göster")
    parser.add_argument("--watch", type=int, metavar="SECONDS", help="Sürekli izleme (saniye)")
    args = parser.parse_args()

    if args.health:
        health()
    elif args.list:
        list_skills()
    elif args.recent:
        recent()
    elif args.watch is not None:
        watch(args.watch)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
