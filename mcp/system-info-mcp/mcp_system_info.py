#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system-info-mcp — Sistem bilgisi ve sağlık MCP sunucusu.

Stdio üzerinden JSON-RPC 2.0 protokolünü kullanır. Ajaların CPU, RAM, disk,
ağ ve işlem bilgilerini alabilmesi için tool'lar sunar.

Tools:
- sys.health: genel sistem sağlığı özeti (CPU/RAM/disk/ağ)
- sys.cpu: CPU kullanımı ve yük
- sys.memory: bellek (RAM) kullanımı
- sys.disk: disk kullanımı
- sys.processes: en çok kaynak tüketen işlemler
- sys.net: ağ bağlantı durumu
"""

import json
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime


def log(msg):
    print(f"[system-info-mcp] {msg}", file=sys.stderr)


def run_cmd(cmd, timeout=10):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True,
                                text=True, timeout=timeout)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", 124
    except Exception as exc:  # noqa: BLE001
        return str(exc), 1


def response(req_id, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def get_cpu():
    out, _ = run_cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
    try:
        return {"percent": float(out)}
    except ValueError:
        return {"percent": None}


def get_memory():
    out, _ = run_cmd("free -m")
    lines = out.splitlines()
    if len(lines) < 2:
        return {}
    parts = lines[1].split()
    total = int(parts[1]) if len(parts) > 1 else 0
    used = int(parts[2]) if len(parts) > 2 else 0
    free = int(parts[3]) if len(parts) > 3 else 0
    pct = round((used / total) * 100, 1) if total else 0
    return {"total_mb": total, "used_mb": used, "free_mb": free, "percent": pct}


def get_disk(path="/"):
    total, used, free = shutil.disk_usage(path)
    pct = round((used / total) * 100, 1) if total else 0
    return {
        "path": path,
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "percent": pct,
    }


def get_network():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "online"
    except OSError:
        return "offline"


def get_processes(limit=5):
    out, _ = run_cmd(f"ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n {limit + 1}")
    return out


def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {}) or {}

    try:
        if method == "initialize":
            response(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "system-info-mcp", "version": "1.0.0"},
            })
        elif method == "tools/list":
            response(req_id, {
                "tools": [
                    {"name": "sys.health", "description": "Genel sistem sağlığı özeti",
                     "inputSchema": {"type": "object", "properties": {}}},
                    {"name": "sys.cpu", "description": "CPU kullanımı ve yük",
                     "inputSchema": {"type": "object", "properties": {}}},
                    {"name": "sys.memory", "description": "Bellek (RAM) kullanımı",
                     "inputSchema": {"type": "object", "properties": {}}},
                    {"name": "sys.disk", "description": "Disk kullanımı",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}}},
                    {"name": "sys.processes", "description": "En çok kaynak tüketen işlemler",
                     "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer"}}}},
                    {"name": "sys.net", "description": "Ağ bağlantı durumu",
                     "inputSchema": {"type": "object", "properties": {}}},
                ]
            })
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {}) or {}

            if name == "sys.health":
                cpu = get_cpu()
                mem = get_memory()
                disk = get_disk("/")
                net = get_network()
                issues = []
                if cpu.get("percent") is not None and cpu["percent"] > 80:
                    issues.append(f"Yüksek CPU: %{cpu['percent']}")
                if mem and mem.get("percent", 0) > 85:
                    issues.append(f"Yüksek bellek: %{mem['percent']}")
                if disk["percent"] > 85:
                    issues.append(f"Disk neredeyse dolu: %{disk['percent']}")
                if net == "offline":
                    issues.append("Ağ bağlantısı yok")
                status = "kritik" if issues else ("uyarı" if cpu.get("percent") and cpu["percent"] > 60 else "iyi")
                response(req_id, {
                    "timestamp": datetime.now().isoformat(),
                    "status": status,
                    "cpu": cpu,
                    "memory": mem,
                    "disk": disk,
                    "network": net,
                    "issues": issues,
                })
            elif name == "sys.cpu":
                response(req_id, get_cpu())
            elif name == "sys.memory":
                response(req_id, get_memory())
            elif name == "sys.disk":
                response(req_id, get_disk(args.get("path", "/")))
            elif name == "sys.processes":
                response(req_id, {"processes": get_processes(args.get("limit", 5))})
            elif name == "sys.net":
                response(req_id, {"network": get_network()})
            else:
                response(req_id, None, {"code": -32601, "message": f"bilinmeyen tool: {name}"})
        else:
            response(req_id, None, {"code": -32601, "message": f"bilinmeyen metod: {method}"})
    except Exception as exc:  # noqa: BLE001
        response(req_id, None, {"code": -32603, "message": str(exc)})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        handle_request(req)


if __name__ == "__main__":
    main()