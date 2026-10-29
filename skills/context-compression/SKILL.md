---
name: context-compression
description: Konuşma bağlamını sıkıştırır, eski/çakışan girişleri temizler, memory.md yönetimi ve proje belleği sağlığını korur. OpenCode context management için tasarlanmıştır.
compatibility: opencode
version: 1.0.0
---

# Context Compression

Konuşma bağlamını sıkıştırır ve proje belleğini yönetir.

## Özellikler
- Konuşma bağlamı durum raporu (`--status`)
- Bağlam özeti (`--summary`)
- Eski/çakışan giriş temizleme (`--clean`)
- Son N satır sıkıştırma (`--compress N`)
- memory.md bölüm güncelleme (`--update-memory BÖLÜM İÇERİK`)

## Kullanım
```bash
python3 context_compressor.py --status
python3 context_compressor.py --summary
python3 context_compressor.py --clean
python3 context_compressor.py --compress 100
python3 context_compressor.py --update-memory "Yeni Bölüm" "İçerik buraya yazılır"
```

## Dosyalar
- `context_compressor.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
