# agent-duo-app — 2 Ajanın Kullanabileceği Uygulama

Sadece 2 alt-ajen (code-reviewer + security-auditor) tarafından çağrılabilen,
daha odaklı ve basit bir kod inceleme uygulamasıdır.

## Amaç

2 ajanın aynı kod dosyasını bağımsız olarak incelemesi, bulgularının karşılaştırılması
ve tek bir rapor sunması için tasarlandı.

## Yapı

```
agent-duo-app/
├── app.py            # Ana uygulama (duo koordine eder)
├── duo.py            # 2 ajanı çalıştıran ve sonuçları birleştiren
├── agents/
│   ├── reviewer.py   # Kod kalitesi inceleme ajanı
│   └── auditor.py    # Güvenlik denetim ajanı
└── reports/          # Çıktı raporları
```

## Kurulum

```bash
chmod +x agent-duo-app/app.py
```

## Kullanım

```bash
# 2 ajanı (reviewer + auditor) bir dosya üzerinde çalıştır
python3 agent-duo-app/app.py --target /path/to/dosya.py

# JSON rapor al
python3 agent-duo-app/app.py --target /path/to/dosya.py --json
```

## Çıktı

Her ajanın bulgu dosyası `reports/` dizinine kaydedilir. Ekrana iki ajanın da
bulgularını içeren bir özet yazdırılır.

## Not

Bu uygulama sadece 2 ajan tarafından çağrılmak üzere sınırlıdır. Daha fazla
ajan için `agent-toolkit/` (5 ajan) kullanın.