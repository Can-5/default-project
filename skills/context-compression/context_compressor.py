#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
context-compression — Konuşma bağlamını sıkıştırır, eski/çakışan girişleri temizler,
memory.md yönetimi ve proje belleği sağlığını korur. OpenCode context management için tasarlanmıştır.
"""
import argparse
import sys
from pathlib import Path

MEMORY_FILE = Path.cwd() / "memory.md"


def status():
    print("=== Bağlam Durumu ===")
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
        print(f"memory.md: {len(content)} karakter, {len(content.splitlines())} satır")
    else:
        print("memory.md bulunamadı.")


def summary():
    print("=== Bağlam Özeti ===")
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
        words = len(content.split())
        print(f"Kelime sayısı: {words}")
        print(f"İlk 200 karakter: {content[:200]}")
    else:
        print("memory.md bulunamadı.")


def clean():
    print("=== Eski/Çakışan Giriş Temizliği ===")
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
        lines = content.splitlines()
        cleaned = [l for l in lines if l.strip()]
        MEMORY_FILE.write_text("\n".join(cleaned), encoding="utf-8")
        print(f"Temizlenen boş satır: {len(lines) - len(cleaned)}")
    else:
        print("memory.md bulunamadı.")


def compress(n: int):
    print(f"=== Bağlam Sıkıştırma (son {n} satır) ===")
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
        lines = content.splitlines()
        compressed = lines[-n:] if n < len(lines) else lines
        MEMORY_FILE.write_text("\n".join(compressed), encoding="utf-8")
        print(f"Sıkıştırıldı: {len(lines)} → {len(compressed)} satır")
    else:
        print("memory.md bulunamadı.")


def update_memory(section: str, content_text: str):
    print(f"=== memory.md Güncelleme: {section} ===")
    if MEMORY_FILE.exists():
        old = MEMORY_FILE.read_text(encoding="utf-8")
    else:
        old = ""
    new_entry = f"\n## {section}\n{content_text}\n"
    MEMORY_FILE.write_text(old + new_entry, encoding="utf-8")
    print(f"Bölüm eklendi/güncellendi: {section}")


def main():
    parser = argparse.ArgumentParser(description="Context Compression")
    parser.add_argument("--status", action="store_true", help="Bağlam durumunu göster")
    parser.add_argument("--summary", action="store_true", help="Bağlam özetini göster")
    parser.add_argument("--clean", action="store_true", help="Eski/çakışan girişleri temizle")
    parser.add_argument("--compress", type=int, metavar="N", help="Son N satırı sıkıştır")
    parser.add_argument("--update-memory", nargs=2, metavar=("BÖLÜM", "İÇERİK"), help="memory.md güncelle")
    args = parser.parse_args()

    if args.status:
        status()
    elif args.summary:
        summary()
    elif args.clean:
        clean()
    elif args.compress is not None:
        compress(args.compress)
    elif args.update_memory:
        update_memory(args.update_memory[0], args.update_memory[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
