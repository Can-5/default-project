---
name: system-doctor
description: Sistem sağlığı teşhisi aracı. CPU, RAM, disk, ağ ve işlem durumunu raporlar.
compatibility: opencode
version: 1.0.0
---

# system-doctor

Sistem sağlığını teşhis etmek için kullanılan bir OpenCode skill'idir.

## Özellikler

- CPU kullanım yüzdesi
- Bellek (RAM) kullanımı
- Disk kullanımı (/)
- Ağ bağlantı durumu
- En çok CPU tüketen işlemler
- Genel sağlık durumu (iyi / uyarı / kritik)

## Kurulum

```bash
chmod +x skills/system-doctor/system_doctor.py
```

## Kullanım

```bash
python3 skills/system-doctor/system_doctor.py --health
python3 skills/system-doctor/system_doctor.py --json
python3 skills/system-doctor/system_doctor.py --processes
```

## Parametreler

| Parametre | Açıklama |
|---|---|
| `--health` | Sağlık özetini gösterir |
| `--json` | Çıkışı JSON olarak verir |
| `--processes` | En çok CPU tüketen işlemleri listeler |

## Örnek Çıktı

```
Durum: İYI
CPU: %12.5
Bellek: %45.2 (3450/7632 MB)
Disk (/): %68.1 (45.2/66.4 GB)
Ağ: online
```
