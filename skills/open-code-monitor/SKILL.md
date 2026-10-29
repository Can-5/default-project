---
name: open-code-monitor
description: OpenCode oturumlarını, skill kullanımını ve sistem sağlığını izler. Gerçek zamanlı izleme, uyarı ve sağlık kontrolü sağlar.
compatibility: opencode
version: 1.0.0
---

# OpenCode Monitor

OpenCode oturumlarını, skill kullanımını ve sistem sağlığını izler.

## Özellikler
- Sağlık kontrolü (`--health`)
- Skill listesi (`--list`)
- Son işlemler (`--recent`)
- Sürekli izleme (`--watch`)

## Kullanım
```bash
python3 open_code_monitor.py --health
python3 open_code_monitor.py --list
python3 open_code_monitor.py --watch 5
```

## Dosyalar
- `open_code_monitor.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
