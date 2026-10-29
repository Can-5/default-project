---
name: auto-skill-manager
description: OpenCode skill'lerini otomatik yönetir. Kur, sil, listele, denetle ve güncelle işlemlerini tek komutla yapar.
compatibility: opencode
version: 1.0.0
---

# Auto Skill Manager

OpenCode skill'lerini otomatik yönetir.

## Özellikler
- Skill listeleme (`list`)
- Skill denetimi (`check`)
- Skill kurulumu (`install`)
- Skill kaldırma (`remove`)

## Kullanım
```bash
python3 auto_skill_manager.py list
python3 auto_skill_manager.py check skill-adi
python3 auto_skill_manager.py install /kaynak/dizin
python3 auto_skill_manager.py remove skill-adi
```

## Dosyalar
- `auto_skill_manager.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
