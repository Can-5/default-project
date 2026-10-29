---
name: ai-token-optimizer
description: Yapay zeka token tüketimini analiz eder ve optimize eder. İstemleri (prompt) inceleyerek gereksiz token'ları azaltır, bütçe yönetimi ve verimlilik ipuçları sağlar.
compatibility: opencode
version: 1.0.0
---

# AI Token Optimizer

Yapay zeka modellerinin tükettiği token miktarını analiz eder ve optimizasyon önerileri sunar.

## Özellikler
- İstem analizi (karakter, kelime, token sayısı, satır)
- İstem optimizasyonu (gereksiz boşluk ve tekrarlanan satır temizliği)
- Token tasarruf raporu (önce/sonra karşılaştırması)
- 10 adet verimlilik ipucu
- `--analyze`, `--optimize`, `--output`, `--tips` parametreleri

## Kullanım
```bash
python3 ai_token_optimizer.py --analyze istem.txt
python3 ai_token_optimizer.py --optimize istem.txt --output optimize.txt
python3 ai_token_optimizer.py --tips
```

## Dosyalar
- `ai_token_optimizer.py` — Ana skill dosyası
- `SKILL.md` — Skill belgeleri
