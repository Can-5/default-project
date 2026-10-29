#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fs-monitor-mcp — Dosya sistemi izleme MCP sunucusu.

Stdio üzerinden JSON-RPC 2.0 protokolünü kullanır. Ajaların
dosya/dizin oluşturma, silme, değişiklik ve varlık denetimlerini yapabilmesi
için tool'lar sunar.

Tools:
- fs.exists: bir yolun varlığını denetler
- fs.list: bir dizinin içeriğini listeler
- fs.read: bir dosyanın içeriğini okur
- fs.write: bir dosyaya içerik yazar
- fs.mkdir: bir dizin oluşturur
- fs.remove: bir dosya veya boş dizini siler
"""

import json
import os
import sys
from pathlib import Path

WORKSPACE = Path(os.environ.get("MCP_FS_WORKSPACE", "/home/ilkaycan/Belgeler/Default Project")).resolve()


def log(msg):
    print(f"[fs-monitor-mcp] {msg}", file=sys.stderr)


def response(req_id, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {}) or {}

    try:
        if method == "initialize":
            response(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "fs-monitor-mcp", "version": "1.0.0"},
            })
        elif method == "tools/list":
            response(req_id, {
                "tools": [
                    {"name": "fs.exists", "description": "Bir yolun varlığını denetler",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                    {"name": "fs.list", "description": "Bir dizinin içeriğini listeler",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                    {"name": "fs.read", "description": "Bir dosyanın içeriğini okur",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                    {"name": "fs.write", "description": "Bir dosyaya içerik yazar",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
                    {"name": "fs.mkdir", "description": "Bir dizin oluşturur",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                    {"name": "fs.remove", "description": "Bir dosya veya boş dizini siler",
                     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                ]
            })
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {}) or {}
            path_str = args.get("path", "")
            try:
                target = (WORKSPACE / path_str).resolve()
                if not str(target).startswith(str(WORKSPACE)):
                    raise ValueError("yol workspace dışında")
            except Exception as exc:
                response(req_id, None, {"code": -32602, "message": f"geçersiz yol: {exc}"})
                return

            if name == "fs.exists":
                response(req_id, {"exists": target.exists(), "is_dir": target.is_dir(), "is_file": target.is_file()})
            elif name == "fs.list":
                if not target.is_dir():
                    response(req_id, None, {"code": -32600, "message": "dizin değil"})
                    return
                items = []
                for child in sorted(target.iterdir()):
                    items.append({"name": child.name, "type": "dir" if child.is_dir() else "file"})
                response(req_id, {"items": items})
            elif name == "fs.read":
                if not target.is_file():
                    response(req_id, None, {"code": -32600, "message": "dosya değil"})
                    return
                content = target.read_text(encoding="utf-8", errors="ignore")
                response(req_id, {"content": content})
            elif name == "fs.write":
                content = args.get("content", "")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                response(req_id, {"written": len(content)})
            elif name == "fs.mkdir":
                target.mkdir(parents=True, exist_ok=True)
                response(req_id, {"created": str(target)})
            elif name == "fs.remove":
                if target.is_dir():
                    target.rmdir()
                else:
                    target.unlink()
                response(req_id, {"removed": str(target)})
            else:
                response(req_id, None, {"code": -32601, "message": f"bilinmeyen tool: {name}"})
        else:
            response(req_id, None, {"code": -32601, "message": f"bilinmeyen metod: {method}"})
    except Exception as exc:  # noqa: BLE001
        response(req_id, None, {"code": -32603, "message": str(exc)})


def main():
    log(f"workspace: {WORKSPACE}")
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