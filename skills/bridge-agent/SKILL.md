---
name: bridge-agent
description: Linux Bridge'i OpenCode alt ajanları tarafından kullanılabilir hale getirir. Gerçek CakyOS host'ta pacman, tarayıcı, ekran görüntüsü ve shell komutlarını çalıştırma yetkisi sağlar.
compatibility: opencode
version: 1.0.0
---

# Bridge Agent

Linux Bridge'i OpenCode alt ajanları tarafından kullanılabilir hale getirir.

## Ön Koşul
`bridge_host.py` gerçek CakyOS masaüstü terminalinde çalışmalı:

```bash
cd /home/ilkaycan/Belgeler/Default Project/linux-bridge
python3 bridge_host.py
```

## Özellikler
- Shell komutu çalıştırma (`shell`)
- Tarayıcı açma (`browser` — firefox, chromium vb.)
- Ekran görüntüsü alma (`screenshot`)
- Pacman komutu çalıştırma (`pacman`)
- Host araç durumu kontrolü (`check` — bridge_host.py üzerinden)

## Kullanım
```bash
python3 bridge_agent.py shell "whoami"
python3 bridge_agent.py browser firefox
python3 bridge_agent.py screenshot ekran.png
python3 bridge_agent.py pacman -Syu
```

## Dosyalar
- `bridge_agent.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
- `config/bridge_config.json` — Köprü yapılandırması
