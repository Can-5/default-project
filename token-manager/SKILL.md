---
name: token-manager
description: "Güvenli token/secret yönetim aracı. SHA-256 hash ile saklama, rotasyon, .env desteği, rolleriyle yetki kontrolü. AI token verimliliği öğreticisi ve bütçe yönetimi dahil. Kendine kendine kurulabilir ve test edilebilir."
compatibility: opencode
version: 1.1.0
---

# Token Manager Skill — Güvenli Token/Secret Yönetimi

Bu skill, OpenCode ortamında token, API anahtarı, şifre ve secret'ları güvenli bir şekilde yönetmenizi sağlar.

## Özellikler

- **Token ekleme/listeleme/silme** — SHA-256 hash ile saklama (açık metin yazılmaz)
- **Token rotasyonu** — Mevcut token'ı yeni değerle değiştirme
- **Token doğrulama** — Girilen değerin hash'iyle karşılaştırma
- **.env yönetimi** — Environment variable'ları .env dosyasına ekleme/okuma/listeleme
- **Rol tabanlı yetki kontrolü** — admin, user, viewer rolleri
- **Kendine kendine kurulum** — `--install` ile gerekli dizinler ve varsayılanları oluşturur
- **İşlem günlüğü** — Tüm işlemler `data/token_manager.log` dosyasına kaydedilir

## Dosya Yapısı

```
token-manager/
├── SKILL.md              # Bu dosya (skill tanımı)
├── token_manager.py      # Ana token yönetim motoru
├── data/
│   ├── tokens.json       # Token hash'leri (sadece hash, açık metin yok)
│   └── token_manager.log # İşlem günlüğü
├── .env                  # Environment variable'ları (chmod 600)
└── .gitignore            # data/, .env, logs hariç
```

## Kurulum

```bash
cd token-manager
python3 token_manager.py install
```

Varsayılan admin token oluşturulur: `system` / şifre `token-manager-change-me`
İlk işlem olarak şifreyi değiştirin:

```bash
python3 token_manager.py rotate system <yeni-sifre> system token-manager-change-me
```

## Kullanım Örnekleri

```bash
# Kurulum
python3 token_manager.py install

# Token ekle
python3 token_manager.py add github_pat <token-degeri> admin
python3 token_manager.py add openai_api_key <anahtar> user

# Tokenleri listele (sadece isim ve rol görünür, hash gizli)
python3 token_manager.py list

# Token doğrula
python3 token_manager.py verify github_pat <token-degeri>

# Token rotasyonu (admin gerekli)
python3 token_manager.py rotate github_pat <yeni-token> system <admin-sifre>

# Token sil
python3 token_manager.py delete eski_token system <admin-sifre>

# .env'e environment variable ekle
python3 token_manager.py env-set GITHUB_TOKEN <token>
python3 token_manager.py env-get GITHUB_TOKEN
python3 token_manager.py env-list
```

## Güvenlik

- Token/secretler **asla açık metin yazılmaz**, sadece SHA-256 hash saklanır
- `.env` dosyası `chmod 600` ile sadece sahte okunabilir/yazılabilir
- `.gitignore` ile `data/`, `.env` depodan hariç tutulur
- Yetki kontrolü: sadece `admin` rotasyon/silme yapabilir

## AI Token Verimliliği

Token Manager, AI (yapay zeka) token tüketimini izlemeyi ve verimli kullanmayı öğretir:

### Komutlar

| Komut | Açıklama |
|-------|----------|
| `usage-report` | Günlük AI token kullanım raporunu gösterir (girdi/çıkış token, çağrı sayısı, maliyet) |
| `budget [limit]` | Günlük token bütçesini gösterir veya yeni limit ayarlar |
| `token-tips` | AI token verimliliği için 10 ipucu listeler |
| `efficiency-check` | Mevcut kullanımı analiz eder ve verimlilik önerisi verir |

### Kullanım Örnekleri

```bash
# Günlük token kullanım raporu
python3 token_manager.py usage-report

# Günlük token bütçesini 50.000'e ayarla
python3 token_manager.py budget 50000

# Token verimliliği ipuçları
python3 token_manager.py token-tips

# Verimlilik analizi
python3 token_manager.py efficiency-check
```

### Token Verimliliği İpuçları (Özet)

1. Kısa ve net istemler yazın, gereksiz açıklamalardan kaçının.
2. Sistem talimatlarını minimized tutun.
3. Aynı bağlamı tekrar göndermeyin; özetleyin.
4. Kod bloğu paylaşırken sadece ilgili fonksiyonu gönderin.
5. Spesifik sorular sorun ("Bu fonksiyondaki hatayı bul").
6. Çoklu adımlı görevleri parçalayın.
7. Yanıt uzunluğunu sınırlayın (max_tokens).
8. Kalıpları (template) hazır tutun ve yeniden kullanın.
9. Bütçenizi günlük olarak izleyin: `token-manager.py budget`.
10. Basit görevler için düşük token tüketimli modelleri tercih edin.

## Dosya Yapısı

```
token-manager/
├── SKILL.md              # Bu dosya (skill tanımı)
├── token_manager.py      # Ana token yönetim motoru
├── data/
│   ├── tokens.json       # Token hash'leri (sadece hash, açık metin yok)
│   ├── token_usage.json  # AI token kullanım kayıtları
│   ├── token_budget.json # Token bütçe ayarları
│   └── token_manager.log # İşlem günlüğü
├── .env                  # Environment variable'ları (chmod 600)
└── .gitignore            # data/, .env, logs hariç
```

## Ön Koşulları

- Python 3.8+

## Lisans

MIT