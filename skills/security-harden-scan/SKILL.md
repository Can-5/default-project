---
name: security-harden-scan
description: Kod güvenliği taraması ve sertleştirme. eval/exec, hardcoded secret, shell=True, subprocess, SQL injection, XSS ve path traversal kalıplarını tarar.
compatibility: opencode
version: 1.0.0
---

# security-harden-scan

Python kod dosyalarındaki yaygın güvenlik zafiyetlerini tespit eden ve sertleştirme önerisi sunan OpenCode skill'idir.

## Özellikler

- `eval` / `exec` / `compile` kullanım tespiti
- `shell=True` ve `subprocess` komut enjeksiyon riski taraması
- Hardcoded şifre/token/secret taraması (`sk-*`, `AKIA*`, `password=`, `secret=`)
- SQL injection riskli kalıpları (`%` formatı, f-string sorgu)
- XSS riskli kalıpları (`innerHTML`, `document.write`)
- Path traversal (`..`, `os.path.join` dışı dynamic path)
- Dosya bazlı ve klasör bazlı tarama
- JSON ve metin çıktı seçenekleri
- Her bulgu için severity (kritik/yüksek/orta/düşük) ve düzeltme önerisi

## Kurulum

```bash
chmod +x skills/security-harden-scan/security_harden_scan.py
```

## Kullanım

```bash
python3 skills/security-harden-scan/security_harden_scan.py --path /path/to/code
python3 skills/security-harden-scan/security_harden_scan.py --path /path/to/code --json
python3 skills/security-harden-scan/security_harden_scan.py --path /path/to/code --only critical
```

## Parametreler

| Parametre | Açıklama |
|---|---|
| `--path` (zorunlu) | Taranacak dosya veya klasör yolu |
| `--json` | Çıkışı JSON olarak verir |
| `--only` | Sadece belirtilen severity'yi göster (critical, high, medium, low) |
| `--fix` | Otomatik düzeltilebilir kalıpları işaretler (dry-run) |

## Örnek Çıktı

```
[security-harden-scan] Tarama başlıyor: /home/ilkaycan/Belgeler/Default Project/skills
[!CRITICAL] app.py:12 — eval() kullanımı (kod enjeksiyon riski)
[!HIGH] config.py:5 — Hardcoded şifre tespit edildi
[!MEDIUM] utils.py:23 — shell=True ile subprocess çağrısı
[!LOW] views.py:40 — innerHTML kullanımı (XSS riski)
Toplam bulgu: 4 (critical: 1, high: 1, medium: 1, low: 1)
```

## Not

Bu skill sadece statik desen taramasıdır. Üretim ortamına devam etmeden mutlaka manuel güvenlik incelemesi yapın.