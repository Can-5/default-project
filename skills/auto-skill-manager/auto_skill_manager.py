#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-skill-manager — OpenCode skill'lerini otomatik yönetir.
Kur, sil, listele, denetle ve güncelle işlemlerini tek komutla yapar.
"""
import argparse
import shutil
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "skills"


def list_skills():
    print("=== Yüklü Skill'ler ===")
    if SKILLS_DIR.exists():
        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir():
                print(f"  - {d.name}")
    else:
        print("Skills dizini bulunamadı.")


def check_skill(name: str):
    skill_dir = SKILLS_DIR / name
    if not skill_dir.exists():
        print(f"Hata: Skill bulunamadı: {name}")
        return
    skill_md = skill_dir / "SKILL.md"
    py_files = list(skill_dir.glob("*.py"))
    print(f"Skill: {name}")
    print(f"  SKILL.md: {'✅' if skill_md.exists() else '❌'}")
    print(f"  Python dosyaları: {len(py_files)}")
    for f in py_files:
        print(f"    - {f.name}")


def install_skill(source: str):
    src = Path(source)
    if not src.exists():
        print(f"Hata: Kaynak bulunamadı: {source}")
        return
    name = src.name
    dest = SKILLS_DIR / name
    if dest.exists():
        print(f"Uyarı: Skill zaten mevcut: {name}")
        return
    shutil.copytree(src, dest)
    print(f"✅ Skill kuruldu: {name}")


def remove_skill(name: str):
    skill_dir = SKILLS_DIR / name
    if not skill_dir.exists():
        print(f"Hata: Skill bulunamadı: {name}")
        return
    shutil.rmtree(skill_dir)
    print(f"✅ Skill kaldırıldı: {name}")


def main():
    parser = argparse.ArgumentParser(description="Auto Skill Manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="Skill'leri listele")

    p_check = sub.add_parser("check", help="Skill'i denetle")
    p_check.add_argument("name", help="Skill adı")

    p_install = sub.add_parser("install", help="Skill'i kur")
    p_install.add_argument("source", help="Kaynak dizin")

    p_remove = sub.add_parser("remove", help="Skill'i kaldır")
    p_remove.add_argument("name", help="Skill adı")

    args = parser.parse_args()

    if args.command == "list":
        list_skills()
    elif args.command == "check":
        check_skill(args.name)
    elif args.command == "install":
        install_skill(args.source)
    elif args.command == "remove":
        remove_skill(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
