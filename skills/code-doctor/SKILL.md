---
name: code-doctor
description: Kod analiz, bug tespiti ve iyileştirme önerileri. Python dosyalarını tarar ve yaygın sorunları raporlar.
compatibility: opencode
version: 1.0.0
---

# code-doctor

Python kodlarını analiz ederek yaygın sorunları ve iyileştirme alanlarını tespit eden bir skill'dir.

## Özellikler

- `eval()` / `exec()` güvenlik riski tespiti
- `print()` kullanım uyarısı (logging önerisi)
- Boş `except` bloğu tespiti
- Hardcoded şifre / secret / API anahtarı tespiti
- Sözdizimi hatası denetimi
- JSON çıktı desteği

## Kurulum

```bash
chmod +x skills/code-doctor/code_doctor.py
```

## Kullanım

```bash
# Tek dosya analizi
python3 skills/code-doctor/code_doctor.py dosya.py

# Tüm proje analizi
python3 skills/code-doctor/code_doctor.py /path/to/proje

# JSON çıktısı
python3 skills/code-doctor/code_doctor.py /path/to/proje --json
```

## Parametreler

| Parametre | Kısaltma | Açıklama |
|---|---|---|
| `path` | | Python dosyası veya dizin yolu (zorunlu) |
| `--json` | | Çıkışı JSON formatında verir |

## Örnek Çıktı

```
📄 app.py
  🟠 Satır 45 [yüksek]: eval() kullanımı güvenlik riski oluşturabilir.
  🟢 Satır 102 [düşük]: print() kullanımı bulundu; logging kullanılması önerilir.
  🔴 Satır 210 [kritik]: Hardcoded API_KEY değeri tespit edildi.

✅ Toplam tespit edilen sorun: 3
```

## Not

Bu skill statik analiz yapar, kod çalıştırılmaz. Tüm uyarılar manuel gözden geçirilmelidir.
