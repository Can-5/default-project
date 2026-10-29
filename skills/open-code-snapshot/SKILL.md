---
name: open-code-snapshot
description: OpenCode kurulumunun anlık görüntüsünü alır ve geri yükleme (snapshot/rollback) yapar. skill, agent, command, config ve memory dosyalarını yedekler.
compatibility: opencode
version: 1.0.0
---

# open-code-snapshot

OpenCode ortamının (skill, agent, command, config, memory.md) anlık görüntüsünü alır ve gerekirse geri yükleme (rollback) yapar. Kurulum değişikliklerinden önce yedek almak için tasarlanmıştır.

## Özellikler

- OpenCode skill klasörünün yedeklenmesi
- Özel agent ve komut dosyalarının yedeklenmesi
- opencode.jsonc yapılandırma dosyasının yedeklenmesi
- memory.md ve .omo bellek dosyalarının yedeklenmesi
- Zaman damgalı snapshot klasörleri (`snapshots/YYYYMMDD_HHMMSS/`)
- `snapshot` (yedekle), `list` (yedekleri listele), `restore` (geriye dön) komutları
- Tek komutla tam geri yükleme

## Kurulum

```bash
chmod +x skills/open-code-snapshot/open_code_snapshot.py
```

## Kullanım

```bash
python3 skills/open-code-snapshot/open_code_snapshot.py snapshot
python3 skills/open-code-snapshot/open_code_snapshot.py list
python3 skills/open-code-snapshot/open_code_snapshot.py restore snapshots/20261029_203000
```

## Parametreler

| Parametre | Açıklama |
|---|---|
| `snapshot` | Mevcut OpenCode kurulumunun anlık görüntüsünü alır |
| `list` | Mevcut snapshot'ları listeler |
| `restore <klasör>` | Belirtilen snapshot'ı geri yükler |

## Örnek Çıktı

```
[open-code-snapshot] Snapshot oluşturuluyor...
[open-code-snapshot] 12 skill, 7 agent, 7 komut, 1 config, 1 memory yedeklendi.
[open-code-snapshot] Konum: snapshots/20261029_203000/
[open-code-snapshot] Tamamlandı.
```

## Not

Snapshot'lar `/home/ilkaycan/Belgeler/Default Project/snapshots/` dizinine yazılır. Geri yükleme işlemi mevcut dosyaların üzerine yazar; önce elinizdeki değişiklikleri kontrol edin.