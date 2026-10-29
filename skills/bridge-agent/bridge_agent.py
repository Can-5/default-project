#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bridge-agent — Linux Bridge'i OpenCode alt ajanları tarafından kullanılabilir hale getirir.
Gerçek CakyOS host'ta pacman, tarayıcı, ekran görüntüsü ve shell komutlarını çalıştırma yetkisi sağlar.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
BRIDGE_DIR = BASE.parent / "linux-bridge"
CMD_DIR = BRIDGE_DIR / "cmd"
RESULT_DIR = BRIDGE_DIR / "result"


def send_command(command: str, ctype: str = "shell") -> dict:
    """bridge_host.py'ye komut gönderir ve sonucu döndürür."""
    CMD_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    cmd_id = f"bridge_{int(time.time() * 1000)}"
    payload = {"id": cmd_id, "command": command, "type": ctype, "ts": time.time()}
    cmd_file = CMD_DIR / f"{cmd_id}.json"
    cmd_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    result_file = RESULT_DIR / f"{cmd_id}.json"
    for _ in range(100):  # 50 saniye bekle
        if result_file.exists():
            result = json.loads(result_file.read_text(encoding="utf-8"))
            result_file.unlink(missing_ok=True)
            return result
        time.sleep(0.5)

    return {"stdout": "", "stderr": "Zaman aşımı", "exitcode": 124}


def shell(command: str) -> dict:
    return send_command(command, "shell")


def browser(browser_name: str) -> dict:
    return send_command(browser_name, "browser")


def screenshot(save_name: str | None = None) -> dict:
    return send_command(save_name or "", "screenshot")


def pacman(args: str) -> dict:
    return send_command(f"pacman {args}", "shell")


def main():
    parser = argparse.ArgumentParser(description="Bridge Agent")
    sub = parser.add_subparsers(dest="command")

    p_shell = sub.add_parser("shell", help="Shell komutu çalıştır")
    p_shell.add_argument("command", help="Komut")

    p_browser = sub.add_parser("browser", help="Tarayıcı aç")
    p_browser.add_argument("name", help="Tarayıcı adı (firefox, chromium vb.)")

    p_screenshot = sub.add_parser("screenshot", help="Ekran görüntüsü al")
    p_screenshot.add_argument("file", nargs="?", help="Kayıt dosya adı")

    p_pacman = sub.add_parser("pacman", help="Pacman komutu çalıştır")
    p_pacman.add_argument("args", help="Pacman argümanları")

    args = parser.parse_args()

    if args.command == "shell":
        result = shell(args.command)
    elif args.command == "browser":
        result = browser(args.name)
    elif args.command == "screenshot":
        result = screenshot(args.file)
    elif args.command == "pacman":
        result = pacman(args.args)
    else:
        parser.print_help()
        return

    print(result.get("stdout", ""))
    if result.get("stderr"):
        print(result["stderr"], file=sys.stderr)
    sys.exit(result.get("exitcode", 0))


if __name__ == "__main__":
    main()
