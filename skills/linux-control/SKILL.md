---
name: linux-control
description: "OpenCode kendi içinde Linux komutlarını çalıştırabilir hale getirir. bridge_host.py + bridge_send.py üzerinden shell, browser, screenshot ve pacman komutlarını gerçek CakyOS masaüstünde yürütür."
compatibility: opencode
version: 1.0.0
---

# Linux Control Skill — OpenCode İçin Linux Komut Kontrolü

Bu skill, OpenCode'un kendi içinde (Flatpak sandbox olmasına rağmen) gerçek CakyOS masaüstü host'unda Linux komutları çalıştırabilmesini sağlar. `bridge_host.py` (gerçek host) + `bridge_send.py` (sandbox istemci) dosya tabanlı komut köprüsü üzerinden çalışır.

## Neden Gerekli?

OpenCode Flatpak sandbox içinde çalışır ve doğrudan host'a erişemez:
- `pacman` komutu yok (Freedesktop SDK runtime içinde)
- `flatpak-spawn --host` engellenebilir (DBus.ServiceUnknown)
- Gerçek tarayıcı açma, ekran görüntüsü alma sadece host'ta mümkün

Linux Control bu sınırlamayı aşar: `cmd/` ve `result/` klasörleri üzerinden dosya tabanlı komut köprüsü kurar.

## Dosya Yapısı

```
skills/linux-control/
├── SKILL.md              # Bu dosya (skill tanımı)
├── linux_control.py      # Ana Linux kontrol motoru
```

## Ön Koşul: bridge_host.py Çalışmalı

Linux Control'i kullanabilmek için `bridge_host.py`'yi **gerçek CakyOS masaüstü terminalinde** çalıştırmanız gerekir:

```bash
cd /home/ilkaycan/Belgeler/Default Project/linux-bridge
python3 bridge_host.py
```

Bu işlem `cmd/` dizinini sürekli izler ve gelen komutları gerçek host üzerinde çalıştırır. Sandbox'tan (OpenCode) bu köprüya bağlanılarak komutlar gönderilir.

## Kullanım Örnekleri (Agent tarafından)

```python
from linux_control import LinuxControl

lc = LinuxControl()

# Shell komutu (pacman, whoami, vb.)
result = lc.shell("pacman -Syu --noconfirm")
print(result)

# Sistem bilgileri
result = lc.whoami()
result = lc.uname()
result = lc.uptime()
result = lc.disk_usage()
result = lc.memory_info()
result = lc.list_processes()

# Tarayıcı aç
result = lc.browser("firefox")

# Ekran görüntüsü al
result = lc.screenshot("masaustu.png")

# Komut satırı üzerinden:
python3 linux_control.py --shell "whoami"
python3 linux_control.py --browser firefox
python3 linux_control.py --screenshot masaustu.png
python3 linux_control.py --pacman "-Syu --noconfirm"
python3 linux_control.py --whoami --uname --uptime --disk --memory --ps
```

## Komut Türleri

| Tür | Açıklama | Örnek |
|-----|----------|-------|
| `shell` | Normal shell komutu (varsayılan) | `pacman -Syu`, `whoami`, `uname -a` |
| `browser` | Belirtilen tarayıcıyı açar | `firefox`, `chromium`, `chrome`, `brave` |
| `screenshot` | Ekran görüntüsü alır | `grim`, `scrot`, `import` ile |

## Kolay Erişim Komutları

- `--shell <komut>` — Herhangi bir shell komutu
- `--whoami` — Mevcut kullanıcıyı gösterir
- `--uname` — Sistem bilgilerini gösterir
- `--uptime` — Sistem çalışma süresini gösterir
- `--disk` — Disk kullanımını gösterir
- `--memory` — Bellek bilgilerini gösterir
- `--ps` — Çalışan işlemleri listeler
- `--browser <isim>` — Tarayıcı açar (firefox, chromium, chrome, brave)
- `--screenshot [dosya.png]` — Ekran görüntüsü alır
- `--pacman <işlem>` — Pacman komutu çalıştırır

## Güvenlik

- Komutlar `shell=True` ile çalıştırılır — sadece güvenilir komutlar gönderilmeli
- Köprü sadece yerel dosya sistemi üzerinden çalışır, ağ erişimi yok
- `bridge_host.py`'yi çalıştıran kullanıcının yetkileriyle komutlar çalışır (pacman için `sudo` gerekebilir)
- Sadece gerçek CakyOS masaüstü terminalinde çalıştırılmalı (Flatpak sandbox içinde doğrudan host erişimi yok)

## Lisans

MIT