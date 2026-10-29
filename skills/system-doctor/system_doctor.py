#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system-doctor — Sistem sağlığı teşhisi aracı.
CPU, RAM, disk, ağ ve işlem durumunu raporlar.
"""

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime


def run_cmd(cmd):
    """Komut çalıştırıp çıkışını döndürür."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True,
                                text=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 124
    except Exception as exc:  # noqa: BLE001
        return "", str(exc), 1


def get_cpu_load():
    """CPU yük yüzdesini döndürür."""
    out, _, _ = run_cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
    try:
        return float(out)
    except ValueError:
        return None


def get_memory_info():
    """Bellek bilgilerini döndürür."""
    out, _, _ = run_cmd("free -m")
    lines = out.splitlines()
    if len(lines) < 2:
        return {}
    parts = lines[1].split()
    if len(parts) < 3:
        return {}
    total = int(parts[1])
    used = int(parts[2])
    free = int(parts[3]) if len(parts) > 3 else 0
    pct = round((used / total) * 100, 1) if total else 0
    return {"total_mb": total, "used_mb": used, "free_mb": free, "percent": pct}


def get_disk_info(path="/"):
    """Disk kullanım bilgilerini döndürür."""
    total, used, free = shutil.disk_usage(path)
    pct = round((used / total) * 100, 1) if total else 0
    return {
        "path": path,
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "percent": pct,
    }


def get_network_info():
    """Basit ağ bağlantı testi (google.com DNS)."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "online"
    except OSError:
        return "offline"


def get_top_processes(limit=5):
    """En çok CPU tüketen işlemleri döndürür."""
    out, _, _ = run_cmd(
        "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n {}".format(limit + 1)
    )
    return out


def health_status():
    """Genel sağlık durumu döndürür."""
    cpu = get_cpu_load()
    mem = get_memory_info()
    disk = get_disk_info("/")
    net = get_network_info()

    issues = []
    if cpu is not None and cpu > 80:
        issues.append(f"Yüksek CPU kullanımı: %{cpu}")
    if mem and mem["percent"] > 85:
        issues.append(f"Yüksek bellek kullanımı: %{mem['percent']}")
    if disk["percent"] > 85:
        issues.append(f"Disk neredeyse dolu: %{disk['percent']}")
    if net == "offline":
        issues.append("Ağ bağlantısı yok")

    status = "kritik" if issues else ("uyarı" if (cpu and cpu > 60) else "iyi")
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu,
        "memory": mem,
        "disk": disk,
        "network": net,
        "status": status,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Sistem sağlığı teşhisi")
    parser.add_argument("--health", action="store_true",
                        help="Sağlık özetini göster")
    parser.add_argument("--json", action="store_true",
                        help="Çıkışı JSON olarak ver")
    parser.add_argument("--processes", action="store_true",
                        help="En çok CPU tüketen işlemleri göster")
    args = parser.parse_args()

    if args.processes or not any([args.health, args.json]):
        print("=== En çok CPU tüketen işlemler ===")
        print(get_top_processes())

    if args.health or args.json:
        data = health_status()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"Durum: {data['status'].upper()}")
            print(f"CPU: %{data['cpu_percent'] if data['cpu_percent'] is not None else '?'}")
            if data["memory"]:
                print(f"Bellek: %{data['memory']['percent']} "
                      f"({data['memory']['used_mb']}/{data['memory']['total_mb']} MB)")
            print(f"Disk (/): %{data['disk']['percent']} "
                  f"({data['disk']['used_gb']}/{data['disk']['total_gb']} GB)")
            print(f"Ağ: {data['network']}")
            if data["issues"]:
                print("Sorunlar:")
                for issue in data["issues"]:
                    print(f"  - {issue}")


if __name__ == "__main__":
    main()
