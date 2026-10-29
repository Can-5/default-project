# agent-toolkit — 5 Ajanın Kullanabileceği Modüler Yazılım

OpenCode alt ajenleri (code-reviewer, security-auditor, debugger, researcher,
devops-engineer) tarafından çağrılabilen, görev dağtıran ve sonuçları birleştiren
modüler bir araç setidir.

## Amaç

5 farklı alt-ajenin aynı kod tabanına bağımsız olarak erişebilmesi, her birinin
özgün bir bulgu seti üretmesi ve bir agregatörün bu bulguları tek rapor haline
getirmesi için tasarlandı.

## Yapı

```
agent-toolkit/
├── dispatcher.py      # 5 ajanı yönlendiren dağıtıcı
├── aggregator.py      # Ajans sonuçlarını tek raporda birleştiren
├── cli.py             # Komut satırı arayüzü
├── agents/
│   ├── reviewer.py    # Kod kalitesi inceleme ajanı
│   ├── security.py    # Güvenlik denetim ajanı
│   ├── debugger.py    # Hata ayıklama ajanı
│   ├── researcher.py  # Araştırma/dökümantasyon ajanı
│   └── devops.py      # Dağıtım/altyapı ajanı
└── reports/           # Çıktı raporları buraya yazılır
```

## Kurulum

```bash
chmod +x agent-toolkit/cli.py
```

## Kullanım (komut satırı)

```bash
# Tüm 5 ajanı bir proje üzerinde çalıştır
python3 agent-toolkit/cli.py --target /path/to/proje --run all

# Sadece belirli ajanı çalıştır
python3 agent-toolkit/cli.py --target /path/to/proje --run security

# JSON rapor al
python3 agent-toolkit/cli.py --target /path/to/proje --run all --json
```

## Kullanım (Python import)

```python
from agent_toolkit.dispatcher import Dispatcher
from agent_toolkit.aggregator import Aggregator

disp = Dispatcher(target="/path/to/proje")
results = disp.run_all()  # veya disp.run("security")

agg = Aggregator(results)
report = agg.build_report()
print(report)
```

## Ajanslar

| Ajan | Görev |
|------|-------|
| reviewer | Kod kalitesi, SOLID, kod koku tespiti |
| security | Güvenlik zafiyeti, hardcoded secret, injection tarama |
| debugger | Hata kalıpları, boş except, print, debug kodu |
| researcher | Dökümantasyon eksikliği, README, yorum kalitesi |
| devops | CI/CD, Docker, ortam yapılandırması |

## Çıktı

Her ajanın kendi bulgu dosyası `reports/<ajan>_<zamandamla>.json` olarak
kaydedilir. Aggregator ise `reports/aggregate_<zamandamla>.json` ve
ekrana okunabilir bir özet yazdırır.

## Not

Bu araç OpenCode alt ajenleri tarafından çağrılmak üzere tasarlandığı için
hiçbir ağ çağrısı yapmaz ve sadece yerel dosya sistemi üzerinde çalışır.