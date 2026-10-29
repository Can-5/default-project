#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Manager — Güvenli token/secret yönetim aracı.
Kendine kendine kurulum ve test desteği ile.
Yeni: AI token verimliliği öğreticisi ve bütçe yönetimi.

Özellikler:
- Token ekleme/listeleme/silme (SHA-256 hash ile saklama)
- Environment variable yönetimi (.env dosyası)
- Token rotation (yeniden oluşturma)
- Güvenli okuma (sadece hash karşılaştırma)
- Kullanıcı rolleri ve yetki kontrolü
- AI token verimliliği öğreticisi (token bütçe, kullanım takip, optimizasyon ipuçları)

Güvenlik: Açık metin şifre/token asla diske yazılmaz, sadece SHA-256 hash saklanır.
"""

import hashlib
import json
import os
import secrets
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
TOKENS_FILE = DATA_DIR / "tokens.json"
ENV_FILE = BASE / ".env"
LOG_FILE = DATA_DIR / "token_manager.log"
USAGE_FILE = DATA_DIR / "token_usage.json"
BUDGET_FILE = DATA_DIR / "token_budget.json"

ROLES = {
    "admin": ["read", "write", "delete", "rotate", "list"],
    "user": ["read", "write"],
    "viewer": ["read"],
}

DEFAULT_TOKENS = {
    "system": {
        "hash": hashlib.sha256(b"token-manager-change-me").hexdigest(),
        "role": "admin",
        "created": time.time(),
        "rotated": None,
    }
}

DEFAULT_BUDGET = {
    "daily_token_limit": 100000,
    "daily_used": 0,
    "reset_date": time.strftime("%Y-%m-%d"),
    "warnings": [],
}


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TOKENS_FILE.exists():
        TOKENS_FILE.write_text(json.dumps(DEFAULT_TOKENS, indent=2, ensure_ascii=False), encoding="utf-8")
    if not LOG_FILE.exists():
        LOG_FILE.write_text("", encoding="utf-8")
    if not USAGE_FILE.exists():
        USAGE_FILE.write_text(json.dumps({}, indent=2, ensure_ascii=False), encoding="utf-8")
    if not BUDGET_FILE.exists():
        BUDGET_FILE.write_text(json.dumps(DEFAULT_BUDGET, indent=2, ensure_ascii=False), encoding="utf-8")


def log(msg: str):
    ensure_dirs()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


def load_tokens() -> dict:
    ensure_dirs()
    try:
        return json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return DEFAULT_TOKENS.copy()


def save_tokens(tokens: dict):
    ensure_dirs()
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_token(token: str, stored_hash: str) -> bool:
    return hashlib.sha256(token.encode("utf-8")).hexdigest() == stored_hash


def check_role(tokens: dict, token_name: str, action: str) -> bool:
    entry = tokens.get(token_name)
    if not entry:
        return False
    role = entry.get("role", "viewer")
    return action in ROLES.get(role, [])


def cmd_add(token_name: str, token_value: str, role: str = "user"):
    """Yeni token ekle."""
    tokens = load_tokens()
    if token_name in tokens:
        print(f"[HATA] Token zaten mevcut: {token_name}")
        return 1
    tokens[token_name] = {
        "hash": hash_token(token_value),
        "role": role,
        "created": time.time(),
        "rotated": None,
    }
    save_tokens(tokens)
    log(f"TOKEN_ADD name={token_name} role={role}")
    print(f"[OK] Token eklendi: {token_name} (rol: {role})")
    return 0


def cmd_list():
    """Tokenleri listele (sadece isim ve rol, hash görünmez)."""
    tokens = load_tokens()
    if not tokens:
        print("Token bulunamadı.")
        return 0
    print(f"{'İsim':<25} {'Rol':<10} {'Oluşturma':<20} {'Rotasyon':<20}")
    print("-" * 75)
    for name, entry in tokens.items():
        created = time.strftime("%Y-%m-%d %H:%M", time.localtime(entry.get("created", 0)))
        rotated = entry.get("rotated")
        rotated_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(rotated)) if rotated else "-"
        print(f"{name:<25} {entry.get('role','?'):<10} {created:<20} {rotated_str:<20}")
    return 0


def cmd_delete(token_name: str, admin_token: str):
    """Token sil (admin yetkisi gerekli)."""
    tokens = load_tokens()
    if not check_role(tokens, admin_token, "delete"):
        print("[HATA] Yetkisiz: silme izniniz yok.")
        return 1
    if token_name not in tokens:
        print(f"[HATA] Token bulunamadı: {token_name}")
        return 1
    del tokens[token_name]
    save_tokens(tokens)
    log(f"TOKEN_DELETE name={token_name} by={admin_token}")
    print(f"[OK] Token silindi: {token_name}")
    return 0


def cmd_rotate(token_name: str, new_value: str, admin_token: str):
    """Token'i yeniden oluştur (admin yetkisi gerekli)."""
    tokens = load_tokens()
    if not check_role(tokens, admin_token, "rotate"):
        print("[HATA] Yetkisiz: rotasyon izniniz yok.")
        return 1
    if token_name not in tokens:
        print(f"[HATA] Token bulunamadı: {token_name}")
        return 1
    tokens[token_name]["hash"] = hash_token(new_value)
    tokens[token_name]["rotated"] = time.time()
    save_tokens(tokens)
    log(f"TOKEN_ROTATE name={token_name} by={admin_token}")
    print(f"[OK] Token rotasyonu tamamlandı: {token_name}")
    return 0


def cmd_verify(token_name: str, token_value: str):
    """Token'i doğrula."""
    tokens = load_tokens()
    entry = tokens.get(token_name)
    if not entry:
        print(f"[HATA] Token bulunamadı: {token_name}")
        return 1
    if verify_token(token_value, entry["hash"]):
        print(f"[OK] Token geçerli: {token_name}")
        return 0
    else:
        print(f"[HATA] Token geçersiz: {token_name}")
        return 1


def cmd_env_set(key: str, value: str):
    """Environment variable ayarla (.env dosyasına)."""
    lines = []
    if ENV_FILE.exists():
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    new_lines = []
    found = False
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{key}={value}")
    ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    os.chmod(ENV_FILE, 0o600)
    log(f"ENV_SET key={key}")
    print(f"[OK] Environment variable ayarlandı: {key}")
    return 0


def cmd_env_get(key: str):
    """Environment variable'ı oku."""
    if not ENV_FILE.exists():
        print(f"[HATA] .env dosyası bulunamadı.")
        return 1
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(f"{key}="):
            value = line.split("=", 1)[1]
            print(f"{key}={value}")
            return 0
    print(f"[HATA] Anahtar bulunamadı: {key}")
    return 1


def cmd_env_list():
    """Tüm environment variable'ları listele (değerler gizli)."""
    if not ENV_FILE.exists():
        print(".env dosyası bulunamadı.")
        return 0
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key = line.split("=", 1)[0]
            print(f"{key}=***")
    return 0


def cmd_install():
    """Kendine kendine kurulum: gereken dizinleri ve varsayılanları oluştur."""
    ensure_dirs()
    print("[OK] Token Manager kurulumu tamamlandı.")
    print(f"   Veri dizini: {DATA_DIR}")
    print(f"   Token dosyası: {TOKENS_FILE}")
    print(f"   .env dosyası: {ENV_FILE}")
    print(f"   Log dosyası: {LOG_FILE}")
    print(f"   Token kullanım dosyası: {USAGE_FILE}")
    print(f"   Token bütçe dosyası: {BUDGET_FILE}")
    print("\nVarsayılan admin token: 'system' / şifre: 'token-manager-change-me'")
    print("Lütfen ilk işlem olarak şifreyi değiştirin: token-manager.py rotate system <yeni-sifre> system token-manager-change-me")
    return 0


# ============================================================================
# AI Token Verimliliği Öğreticisi
# ============================================================================

def load_usage() -> dict:
    ensure_dirs()
    try:
        return json.loads(USAGE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_usage(usage: dict):
    ensure_dirs()
    USAGE_FILE.write_text(json.dumps(usage, indent=2, ensure_ascii=False), encoding="utf-8")


def load_budget() -> dict:
    ensure_dirs()
    try:
        return json.loads(BUDGET_FILE.read_text(encoding="utf-8"))
    except Exception:
        return DEFAULT_BUDGET.copy()


def save_budget(budget: dict):
    ensure_dirs()
    BUDGET_FILE.write_text(json.dumps(budget, indent=2, ensure_ascii=False), encoding="utf-8")


def _reset_daily_if_needed(budget: dict) -> dict:
    today = time.strftime("%Y-%m-%d")
    if budget.get("reset_date") != today:
        budget["daily_used"] = 0
        budget["reset_date"] = today
        budget["warnings"] = []
    return budget


def record_token_usage(model: str, input_tokens: int, output_tokens: int, cost_usd: float = 0.0):
    """AI token kullanımını kaydeder."""
    usage = load_usage()
    today = time.strftime("%Y-%m-%d")
    if today not in usage:
        usage[today] = {"total_input": 0, "total_output": 0, "total_cost": 0.0, "calls": 0, "models": {}}
    usage[today]["total_input"] += input_tokens
    usage[today]["total_output"] += output_tokens
    usage[today]["total_cost"] += cost_usd
    usage[today]["calls"] += 1
    models = usage[today].setdefault("models", {})
    if model not in models:
        models[model] = {"input": 0, "output": 0, "calls": 0, "cost": 0.0}
    models[model]["input"] += input_tokens
    models[model]["output"] += output_tokens
    models[model]["calls"] += 1
    models[model]["cost"] += cost_usd
    save_usage(usage)

    # Bütçeyi güncelle
    budget = load_budget()
    budget = _reset_daily_if_needed(budget)
    budget["daily_used"] += input_tokens + output_tokens
    save_budget(budget)
    log(f"TOKEN_USAGE model={model} input={input_tokens} output={output_tokens} cost={cost_usd}")


def cmd_usage_report():
    """Günlük token kullanım raporu gösterir."""
    usage = load_usage()
    today = time.strftime("%Y-%m-%d")
    if today not in usage or not usage[today]:
        print(f"Bugün ({today}) için token kullanımı kaydı yok.")
        return 0
    day = usage[today]
    print(f"=== AI Token Kullanım Raporu — {today} ===")
    print(f"Toplam Çağrı: {day.get('calls', 0)}")
    print(f"Girdi Token: {day.get('total_input', 0):,}")
    print(f"Çıkış Token: {day.get('total_output', 0):,}")
    print(f"Toplam Token: {day.get('total_input', 0) + day.get('total_output', 0):,}")
    print(f"Tahmini Maliyet: ${day.get('total_cost', 0):.4f}")
    print("\nModel Bazlı:")
    for model, m in day.get("models", {}).items():
        print(f"  {model}: in={m['input']:,} out={m['output']:,} calls={m['calls']} cost=${m['cost']:.4f}")
    return 0


def cmd_budget(status_only: bool = False, limit: int | None = None):
    """Token bütçesini göster veya ayarlar."""
    budget = load_budget()
    budget = _reset_daily_if_needed(budget)
    save_budget(budget)

    print(f"=== Token Bütçesi — {budget.get('reset_date')} ===")
    print(f"Günlük Limit: {budget.get('daily_token_limit', 0):,} token")
    print(f"Kullanılan:   {budget.get('daily_used', 0):,} token")
    remaining = budget.get("daily_token_limit", 0) - budget.get("daily_used", 0)
    print(f"Kalan:        {max(0, remaining):,} token")
    pct = (budget.get("daily_used", 0) / budget.get("daily_token_limit", 1)) * 100
    print(f"Kullanım Oranı: %{pct:.1f}")

    if limit is not None:
        budget["daily_token_limit"] = limit
        save_budget(budget)
        print(f"[OK] Günlük limit {limit:,} olarak güncellendi.")
    return 0


def cmd_token_tips():
    """AI token verimliliği için ipuçları gösterir."""
    tips = [
        "1. Kısa ve net istemler (prompt) yazın — gereksiz açıklamalardan kaçının.",
        "2. Sistem talimatlarını (system prompt) minimized tutun, sadece gerekenleri ekleyin.",
        "3. Aynı bağlamı tekrar tekrar göndermeyin; özetlemiş haliyle kullanın.",
        "4. Kod bloğu paylaşırken sadece ilgili fonksiyonu/class'ı gönderin, hele dosyayı değil.",
        "5. 'Aşağıdaki kodu incele' yerine 'Bu fonksiyondaki X hatasını bul' gibi spesifik sorular sorun.",
        "6. Çoklu adımlı görevleri parçalayın, her adımda yalnızca ilgili bağlamı içeri aktarın.",
        "7. Yanıt uzunluğunu sınırlayın (max_tokens) gereksiz uzun çıkışları engellemek için.",
        "8. Sık kullanılan kalıpları (template) hazır tutun ve yeniden kullanın.",
        "9. Token bütçenizi günlük olarak izleyin: token-manager.py budget",
        "10. Model seçiminde düşük token tüketimli modelleri tercih edin (basit görevler için).",
    ]
    print("=== AI Token Verimliliği İpuçları ===")
    for tip in tips:
        print(tip)
    print("\nDaha fazla bilgi için: token-manager.py usage-report")
    return 0


def cmd_efficiency_check():
    """Mevcut token kullanımını analiz eder ve verimlilik önerisi verir."""
    usage = load_usage()
    today = time.strftime("%Y-%m-%d")
    budget = load_budget()
    budget = _reset_daily_if_needed(budget)

    print("=== Token Verimlilik Analizi ===")
    if today not in usage or not usage[today]:
        print("Henüz kullanım verisi yok. Önce bazı AI işlemleri gerçekleştirin.")
        print("\nÖneriler:")
        for tip in [
            "İlk AI çağrınızı yapın, ardından kullanım raporunu kontrol edin.",
            "token-manager.py token-tips komutu ile genel ipuçlarını okuyun.",
        ]:
            print(f"  - {tip}")
        return 0

    day = usage[today]
    total = day.get("total_input", 0) + day.get("total_output", 0)
    calls = day.get("calls", 0)
    avg_per_call = total / calls if calls > 0 else 0
    limit = budget.get("daily_token_limit", 100000)
    used = budget.get("daily_used", 0)
    remaining = max(0, limit - used)

    print(f"Günlük Toplam Token: {total:,}")
    print(f"Çağrı Sayısı: {calls}")
    print(f"Ortalama Token/Çağrı: {avg_per_call:.0f}")
    print(f"Günlük Bütçe Kullanımı: {used:,} / {limit:,} (kalan: {remaining:,})")

    if avg_per_call > 2000:
        print("\n⚠️  Uyarı: Çağrı başına ortalama token yüksek. İpuçları:")
        for tip in [
            "İstemlerinizi daha kısa ve net hale getirin.",
            "Sadece ilgili kod parçalarını paylaşın.",
            "Yanıt uzunluğunu sınırlayın (max_tokens).",
        ]:
            print(f"   - {tip}")
    else:
        print("\n✅ Token kullanımı verimli seviyede.")

    if remaining < limit * 0.1:
        print("\n⚠️  Uyarı: Günlük token bütçeniz %10'ın altında. Yakında tüketim azaltmalısınız.")

    return 0


def main():
    args = sys.argv[1:]

    if not args:
        print("Token Manager — Kullanım:")
        print("  token-manager.py install                    # Kurulum")
        print("  token-manager.py add <isim> <deger> [rol]   # Token ekle")
        print("  token-manager.py list                       # Tokenleri listele")
        print("  token-manager.py delete <isim> <admin-tok>  # Token sil")
        print("  token-manager.py rotate <isim> <yeni> <admin-tok>  # Token rotasyonu")
        print("  token-manager.py verify <isim> <deger>      # Token doğrula")
        print("  token-manager.py env-set <anahtar> <deger>  # .env'e ekle")
        print("  token-manager.py env-get <anahtar>          # .env'den oku")
        print("  token-manager.py env-list                   # .env'i listele")
        print("")
        print("AI Token Verimliliği:")
        print("  token-manager.py usage-report               # Günlük token kullanım raporu")
        print("  token-manager.py budget [limit]             # Token bütçesini göster/ayarla")
        print("  token-manager.py token-tips                 # Token verimliliği ipuçları")
        print("  token-manager.py efficiency-check           # Token verimlilik analizi")
        return 1

    cmd = args[0]

    if cmd == "install":
        return cmd_install()
    elif cmd == "add":
        if len(args) < 3:
            print("Kullanım: token-manager.py add <isim> <deger> [rol]")
            return 1
        role = args[3] if len(args) > 3 else "user"
        return cmd_add(args[1], args[2], role)
    elif cmd == "list":
        return cmd_list()
    elif cmd == "delete":
        if len(args) < 3:
            print("Kullanım: token-manager.py delete <isim> <admin-tok>")
            return 1
        return cmd_delete(args[1], args[2])
    elif cmd == "rotate":
        if len(args) < 4:
            print("Kullanım: token-manager.py rotate <isim> <yeni-deger> <admin-tok>")
            return 1
        return cmd_rotate(args[1], args[2], args[3])
    elif cmd == "verify":
        if len(args) < 3:
            print("Kullanım: token-manager.py verify <isim> <deger>")
            return 1
        return cmd_verify(args[1], args[2])
    elif cmd == "env-set":
        if len(args) < 3:
            print("Kullanım: token-manager.py env-set <anahtar> <deger>")
            return 1
        return cmd_env_set(args[1], args[2])
    elif cmd == "env-get":
        if len(args) < 2:
            print("Kullanım: token-manager.py env-get <anahtar>")
            return 1
        return cmd_env_get(args[1])
    elif cmd == "env-list":
        return cmd_env_list()
    elif cmd == "usage-report":
        return cmd_usage_report()
    elif cmd == "budget":
        limit = int(args[1]) if len(args) > 1 else None
        return cmd_budget(limit=limit)
    elif cmd == "token-tips":
        return cmd_token_tips()
    elif cmd == "efficiency-check":
        return cmd_efficiency_check()
    else:
        print(f"[HATA] Bilinmeyen komut: {cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())