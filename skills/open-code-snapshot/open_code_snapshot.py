#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open-code-snapshot — OpenCode kurulum anlık görüntüsü ve geri yükleme.

skill, agent, command, config ve memory.md dosyalarını zaman damalıklı
snapshot klasörlerine yedekler ve geri yükler.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Default Project
SNAPSHOT_DIR = BASE_DIR / "snapshots"

OPENCODE_CONFIG = BASE_DIR / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "opencode.jsonc"
OPENCODE_SKILLS = BASE_DIR / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "skills"
OPENCODE_AGENTS = BASE_DIR / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "agents"
OPENCODE_COMMANDS = BASE_DIR / ".var" / "app" / "ai.opencode.opencode" / "config" / "opencode" / "commands"
MEMORY_FILE = BASE_DIR / "memory.md"
OMO_DIR = BASE_DIR / ".omo"

LOCAL_SKILLS = BASE_DIR / "skills"
LOCAL_AGENTS = BASE_DIR / ".opencode" / "agent" if False else BASE_DIR / ".opencode" / "command"


def log(msg):
    print(f"[open-code-snapshot] {msg}")


def ensure_snapshot_dir(name):
    target = SNAPSHOT_DIR / name
    target.mkdir(parents=True, exist_ok=True)
    return target


def copy_tree(src, dst):
    if not src.exists():
        log(f"Uyarı: kaynak bulunamadı, atlanıyor: {src}")
        return 0
    count = 0
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            out = dst / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out)
            count += 1
    return count


def copy_file(src, dst):
    if not src.exists():
        log(f"Uyarı: kaynak bulunamadı, atlanıyor: {src}")
        return 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return 1


def snapshot():
    """Mevcut OpenCode kurulumunun anlık görüntüsünü alır."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = ensure_snapshot_dir(stamp)

    total = 0
    total += copy_tree(OPENCODE_SKILLS, target / "skills")
    total += copy_tree(OPENCODE_AGENTS, target / "agents")
    total += copy_tree(OPENCODE_COMMANDS, target / "commands")
    total += copy_file(OPENCODE_CONFIG, target / "config" / "opencode.jsonc")
    total += copy_file(MEMORY_FILE, target / "memory.md")
    total += copy_tree(OMO_DIR, target / "omo")

    # Yerel skill/agent dosyaları (bu repodaki)
    total += copy_tree(LOCAL_SKILLS, target / "local_skills")

    log(f"{total} dosya yedeklendi.")
    log(f"Konum: {target}")
    log("Tamamlandı.")
    return 0


def list_snapshots():
    """Mevcut snapshot'ları listeler."""
    if not SNAPSHOT_DIR.exists():
        print("Henüz snapshot yok.")
        return 0
    snaps = sorted([p for p in SNAPSHOT_DIR.iterdir() if p.is_dir()], reverse=True)
    if not snaps:
        print("Henüz snapshot yok.")
        return 0
    print("Mevcut snapshot'lar:")
    for s in snaps:
        print(f"  {s.name}")
    return 0


def restore(snapshot_name):
    """Belirtilen snapshot'ı geri yükler."""
    target = SNAPSHOT_DIR / snapshot_name
    if not target.exists():
        print(f"Hata: snapshot bulunamadı: {target}", file=sys.stderr)
        return 1

    total = 0
    total += copy_tree(target / "skills", OPENCODE_SKILLS)
    total += copy_tree(target / "agents", OPENCODE_AGENTS)
    total += copy_tree(target / "commands", OPENCODE_COMMANDS)
    total += copy_file(target / "config" / "opencode.jsonc", OPENCODE_CONFIG)
    total += copy_file(target / "memory.md", MEMORY_FILE)
    total += copy_tree(target / "omo", OMO_DIR)
    total += copy_tree(target / "local_skills", LOCAL_SKILLS)

    log(f"{total} dosya geri yüklendi.")
    log("NOT: Değişikliklerin etkili olması için OpenCode'u yeniden başlatın.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="OpenCode kurulum anlık görüntüsü ve geri yükleme")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("snapshot", help="Anlık görüntü al")
    sub.add_parser("list", help="Snapshot'ları listele")
    p_restore = sub.add_parser("restore", help="Snapshot'ı geri yükle")
    p_restore.add_argument("folder", help="Snapshot klasör adı (örn. snapshots/20261029_203000)")

    args = parser.parse_args()

    if args.command == "snapshot":
        return snapshot()
    if args.command == "list":
        return list_snapshots()
    if args.command == "restore":
        folder = args.folder
        if folder.startswith("snapshots/"):
            folder = folder[len("snapshots/"):]
        return restore(folder)

    return 1


if __name__ == "__main__":
    sys.exit(main())