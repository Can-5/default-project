---
name: ultra-skill
description: Neredeyse her şeyi yapan, kod yazan, alt ajan çağıran, bug düzelten ve linux bridge ile entegre olan ultra güçlü skill. OpenCode ortamını kendi kendine yönetir, geliştirir ve güçlendirir.
compatibility: opencode
version: 1.0.0
---

# Ultra Skill

Neredeyse her şeyi yapan ultra güçlü skill.

## Özellikler
- Kod yazma (`--write-code`)
- Alt ajen çağırma (`--call-agent`)
- Bug düzeltme (`--fix-bug`)
- Linux bridge entegrasyonu (`--bridge`)
- Token yönetimi (`--token`)
- Kendine kurulum (`--self-install`)
- Kendine test (`--self-test`)

## Kullanım
```bash
python3 ultra_skill.py --self-install
python3 ultra_skill.py --self-test
python3 ultra_skill.py --write-code "merhaba dünya"
python3 ultra_skill.py --call-agent code-reviewer "kodu incele"
python3 ultra_skill.py --fix-bug "import hatası"
python3 ultra_skill.py --bridge "whoami"
python3 ultra_skill.py --token usage-report
```

## Dosyalar
- `ultra_skill.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
