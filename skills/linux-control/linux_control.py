#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux Control Skill — OpenCode kendi içinde Linux komutlarını çalıştırabilir hale getirir.
bridge_host.py (gerçek CakyOS masaüstü) + bridge_send.py (sandbox istemci) üzerinden
shell, browser, screenshot ve pacman komutlarını yürütür.

Bu skill, OpenCode alt ajenleri tarafından çağrılabilir. Gerçek host'ta
bridge_host.py çalışmalıdır (Flatpak sandbox doğrudan host erişimi yok).
"""

import argparse
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

# Bridge dosyaları linux-bridge klasöründe
BASE = Path(__file__).resolve().parent.parent.parent  # skills/linux-control -> Default Project
BRIDGE_DIR = BASE / "linux-bridge"
BRIDGE_SEND = BRIDGE_DIR / "bridge_send.py"
BRIDGE_HOST = BRIDGE_DIR / "bridge_host.py"
CMD_DIR = BRIDGE_DIR / "cmd"
RESULT_DIR = BRIDGE_DIR / "result"
SCREENSHOT_DIR = BRIDGE_DIR / "screenshots"
LOG_FILE = BASE / "logs" / "linux_control.log"
DEFAULT_TIMEOUT = 60

# Tarayıcı eşlemesi
BROWSER_MAP = {
    "firefox": "firefox", "ff": "firefox", "mozilla": "firefox",
    "chromium": "chromium", "chrome": "chromium", "google-chrome": "google-chrome",
    "brave": "brave-browser", "opera": "opera",
}


def ensure_dirs():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CMD_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def log(msg: str, level: str = "INFO"):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def host_running() -> bool:
    """bridge_host.py'nin gerçek host'ta çalışıp çalışmadığını kontrol eder."""
    if not BRIDGE_HOST.exists():
        return False
    # cmd/ dizininin yazılabilir olması ve bridge_send.py'nin varlığı yeterli işaret
    return BRIDGE_SEND.exists()


class LinuxControl:
    """Linux komutlarını gerçek CakyOS host'ta çalıştıran kontrol arayüzü."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        ensure_dirs()

    def _send(self, command: str, ctype: str = "shell") -> dict:
        """bridge_send.py üzerinden komut gönderir ve sonucu bekler."""
        if not host_running():
            return {
                "error": "bridge_host.py gerçek CakyOS masaüstü terminalinde çalışmıyor",
                "hint": "cd linux-bridge && python3 bridge_host.py",
                "command": command,
            }

        cmd_id = str(uuid.uuid4())[:8]
        cmd_file = CMD_DIR / f"{cmd_id}.json"
        result_file = RESULT_DIR / f"{cmd_id}.json"

        payload = {"id": cmd_id, "command": command, "type": ctype, "ts": time.time()}
        cmd_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if result_file.exists():
                raw = result_file.read_text(encoding="utf-8")
                result_file.unlink(missing_ok=True)
                return json.loads(raw)
            time.sleep(0.5)

        cmd_file.unlink(missing_ok=True)
        return {"id": cmd_id, "error": "timeout", "command": command}

    def shell(self, command: str) -> dict:
        """Gerçek host'ta shell komutu çalıştırır (pacman, whoami, uname vb.)."""
        log(f"Linux Control shell: {command}")
        return self._send(command, "shell")

    def browser(self, browser_name: str) -> dict:
        """Gerçek host'ta belirtilen tarayıcıyı açar."""
        exe = BROWSER_MAP.get(browser_name.lower().strip(), browser_name)
        log(f"Linux Control browser: {exe}")
        return self._send(exe, "browser")

    def screenshot(self, filename: str = "") -> dict:
        """Gerçek host'tan ekran görüntüsü alır."""
        log(f"Linux Control screenshot: {filename or 'auto'}")
        return self._send(filename if filename else "", "screenshot")

    def pacman(self, operation: str) -> dict:
        """Gerçek host'ta pacman komutu çalıştırır."""
        log(f"Linux Control pacman: {operation}")
        return self._send(f"sudo pacman {operation}", "shell")

    def whoami(self) -> dict:
        return self.shell("whoami")

    def uname(self) -> dict:
        return self.shell("uname -a")

    def uptime(self) -> dict:
        return self.shell("uptime")

    def disk_usage(self) -> dict:
        return self.shell("df -h")

    def memory_info(self) -> dict:
        return self.shell("free -h")

    def list_processes(self) -> dict:
        return self.shell("ps aux")


def print_result(result: dict, label: str = ""):
    if label:
        print(f"=== {label} ===")
    if "error" in result:
        print(f"[HATA] {result['error']}", file=sys.stderr)
        if "hint" in result:
            print(f"[İPUCU] {result['hint']}", file=sys.stderr)
        sys.exit(1)
    print(result.get("stdout", ""))
    if result.get("stderr"):
        print(result["stderr"], file=sys.stderr)
    if result.get("file"):
        print(f"[DOSYA] {result['file']}")
    sys.exit(result.get("exitcode", 0))


def main():
    parser = argparse.ArgumentParser(
        description="Linux Control — OpenCode kendi içinde Linux komutlarını çalıştırır."
    )
    parser.add_argument("--shell", metavar="KOMUT", help="Host'ta shell komutu çalıştırır.")
    parser.add_argument("--whoami", action="store_true", help="Kullanıcıyı gösterir.")
    parser.add_argument("--uname", action="store_true", help="Sistem bilgilerini gösterir.")
    parser.add_argument("--uptime", action="store_true", help="Sistem çalışma süresini gösterir.")
    parser.add_argument("--disk", action="store_true", help="Disk kullanımını gösterir.")
    parser.add_argument("--memory", action="store_true", help="Bellek bilgilerini gösterir.")
    parser.add_argument("--ps", action="store_true", help="Çalışan işlemleri listeler.")
    parser.add_argument("--browser", metavar="TARAYICI", help="Host'ta tarayıcı açar.")
    parser.add_argument("--screenshot", nargs="?", const="", metavar="DOSYA", help="Ekran görüntüsü alır.")
    parser.add_argument("--pacman", metavar="ISLEM", help="Host'ta pacman komutu çalıştırır.")
    args = parser.parse_args()

    lc = LinuxControl()

    if args.shell:
        result = lc.shell(args.shell)
        print_result(result, "Shell Çıktısı")
    if args.whoami:
        result = lc.whoami()
        print_result(result, "Kullanıcı")
    if args.uname:
        result = lc.uname()
        print_result(result, "Sistem")
    if args.uptime:
        result = lc.uptime()
        print_result(result, "Çalışma Süresi")
    if args.disk:
        result = lc.disk_usage()
        print_result(result, "Disk Kullanımı")
    if args.memory:
        result = lc.memory_info()
        print_result(result, "Bellek")
    if args.ps:
        result = lc.list_processes()
        print_result(result, "İşlemler")
    if args.browser:
        result = lc.browser(args.browser)
        print_result(result, "Tarayıcı")
    if args.screenshot is not None:
        result = lc.screenshot(args.screenshot)
        print_result(result, "Ekran Görüntüsü")
    if args.pacman:
        result = lc.pacman(args.pacman)
        print_result(result, "Pacman")

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())