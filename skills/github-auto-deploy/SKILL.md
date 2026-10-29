---
name: github-auto-deploy
description: GitHub otomatik commit + push akışı. Belirtilen dizindeki değişiklikleri commit'leyip push'lar.
compatibility: opencode
version: 1.0.0
---

# github-auto-deploy

GitHub otomatik deploy skill'idir. Belirtilen git deposundaki değişiklikleri commit'leyip push'lar.

## Özellikler

- Tüm değişiklikleri otomatik stage et (`git add -A`)
- Commit mesajı oluştur (varsayılan: tarih/saat ile)
- Belirtilen branch'e checkout ve push
- `--no-push` ile sadece commit yapma seçeneği

## Kurulum

```bash
chmod +x skills/github-auto-deploy/github_auto_deploy.py
```

## Kullanım

```bash
# Temel kullanım (commit + push)
python3 skills/github-auto-deploy/github_auto_deploy.py /path/to/repo

# Özel commit mesajı
python3 skills/github-auto-deploy/github_auto_deploy.py /path/to/repo -m "feat: yeni özellik eklendi"

# Belirli branch'e push
python3 skills/github-auto-deploy/github_auto_deploy.py /path/to/repo -b main

# Sadece commit, push yapma
python3 skills/github-auto-deploy/github_auto_deploy.py /path/to/repo --no-push
```

## Parametreler

| Parametre | Kısaltma | Açıklama |
|---|---|---|
| `path` | | Git reposu dizin yolu (zorunlu) |
| `--message` | `-m` | Özel commit mesajı |
| `--branch` | `-b` | Hedef branch (varsayılan: mevcut) |
| `--no-push` | | Sadece commit et, push yapma |

## Örnek Çıktı

```
Mevcut branch: master
Hedef branch: master
Commit başarılı: auto-deploy: 2026-10-29 14:30:00
Push başarılı: origin/master
```

## Not

Bu skill GitHub CLI (`gh`) gerektirmez, sadece `git` komutunu kullanır. GitHub kimlik doğrulaması için SSH anahtarı veya `gh` CLI ile giriş yapılmış olmalıdır.
