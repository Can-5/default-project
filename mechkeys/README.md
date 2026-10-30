# mechkeys — Mekanik Klavye Ses Simülatörü

CakyOS/Linux masaüstünde klavyedeki her tuş basışında mekanik klavye sesi
çalan, tuş dinleyici bir masaüstü uygulamasıdır.

- **pynput** tuş dinleyici — klavyedeki tuşları yakalar
- **pure-Python ses sentezi** — harici ses dosyası gerekmez (wav bellekte üretilir)
- **Çoklu ses arka ucu** — pygame / paplay / aplay / ffplay / silent
- **Config dosyası** — `config.json` (switch türü, ses, arka uç vb.)
- **CLI** — `--switch`, `--volume`, `--backend`, `--test`, `--no-audio`, `--mock`
- **Gizlilik odaklı** — telemetri yok, sadece yerel, hiçbir tuş verisi dışarıya çıkmıyor
- **Lisans:** MIT

## Kurulum

```bash
# mechkeys klasörüne gir
cd mechkeys

# İsteğe bağlı: sanal ortam
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları yükle (pynput + pygame opsiyonel)
pip install -r requirements.txt
```

> Not: Linux/X11'de tuş dinlemesi için bir X sunucusu (masaüstü) çalışıyor olmalı
> ve `DISPLAY` değişkeni ayarlı olmalıdır. Başlıksız (headless) ortamda
> `--mock` ile test edilebilir.

## Kullanım

```bash
# Varsayılan ayarla çalıştır (mavi switch, ses açık)
python3 mechkeys.py

// Başka bir switch türü
python3 mechkeys.py --switch brown
python3 mechkeys.py --switch red
python3 mechkeys.py --switch black

// Ses seviyesi
python3 mechkeys.py --volume 0.5

// Zorunlu ses arka ucu
python3 mechkeys.py --backend paplay
python3 mechkeys.py --backend aplay

// Sadece test sesi (dinlemez)
python3 mechkeys.py --test

// Tuşları dinle ama ses çıkarma (sadece log)
python3 mechkeys.py --no-audio

// Mock (gerçek dinleyici yok, test için)
python3 mechkeys.py --mock

// Özel config dosyası
python3 mechkeys.py --config /yol/config.json

// Yardım
python3 mechkeys.py --help
```

Çıkış yapmak için: **CTRL+C**  
Ses aç/kapa kısayolu: **F12** (`config.json`'dan `toggle_hotkey` ile değiştirilebilir)

## Yapılandırma (`config.json`)

İlk çalıştırmada otomatik oluşturulur:

```json
{
  "switch": "blue",
  "volume": 0.7,
  "enabled": true,
  "modifiers_silent": true,
  "spacebar_louder": true,
  "audio_backend": "auto",
  "sample_rate": 44100,
  "toggle_hotkey": "f12"
}
```

| Açıklama | Açıklama |
|----------|----------|
| `switch` | `blue` | `brown` | `red` | `black` — anahtar çifti türü |
| `volume` | 0.0 – 1.0 — ses seviyesi |
| `enabled` | ses açık / kapalı |
| `modifiers_silent` | Shift/Ctrl/Alt/Win sessiz |
| `spacebar_louder` | boşluk tuşu daha kuvvetli |
| `audio_backend` | `auto` | `pygame` | `paplay` | `aplay` | `ffplay` | `silent` |
| `sample_rate` | ses örnekleme hızı (44100) |
| `toggle_hotkey` | ses aç/kapa kısayol tuşu |

## Ses Sentezi

Tüm sesler çalışma anında pure-Python (`wave` + `math` + `struct`) ile
üretilir. Harici `.wav` / `.mp3` dosyası **gerekmez**. `sounds/` dizini
isteğe bağlı harici örnekler için ayrılmıştır.

## Gereksinimler

- Python 3.8+
- `pynput` (tuş dinleme)
- `pygame` (ses, opsiyonel — yoksa `paplay`/`aplay`/`ffplay` kullanılır)
- Linux/X11 masaüstü (gerçek tuş dinleme için)

```bash
pip install -r requirements.txt
```

## Gizlilik

Bu uygulama hiçbir veri toplamaz, göndermez veya saklamaz. Tuş basımları
sadece yerelde işlenir ve ses olarak döndürülür. Telemetri, analiz ve
bulut bağlantısı yoktur.

## Lisans

[MIT](LICENSE)
