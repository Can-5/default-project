#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py — mechkeys yapılandırma modülü.

Yapılandırma: config.json dosyasından okunur, yoksa varsayılan değerler
kullanılır ve dosya otomatik olarak oluşturulur. Tüm değerler yereldir,
hiçbir şey dışarıya gönderilmez (gizlilik odaklı).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

# Uygulama dizini (mechkeys/)
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

# Varsayılan yapılandırma
DEFAULTS: Dict[str, Any] = {
    "switch": "blue",           # blue | brown | red | black
    "volume": 0.7,              # 0.0 - 1.0
    "enabled": True,            # Ses açık / kapalı
    "modifiers_silent": True,   # Shift/Ctrl/Alt/Win tuşları sessiz
    "spacebar_louder": True,    # Boşluk tuşu daha kuvvetli ses
    "audio_backend": "auto",    # auto | pygame | paplay | aplay | silent
    "sample_rate": 44100,       # Ses sentezi örnekleme hızı
    "toggle_hotkey": "f12",     # Ses aç/kapa kısayol tuşu
}

# Desteklenen anahtar çifti türleri ve temsili frekansları (Hz)
SWITCH_PRESETS: Dict[str, Dict[str, float]] = {
    "blue": {"click": 0.9, "ping": 1000.0, "decay": 0.12, "volume": 1.0},
    "brown": {"click": 0.5, "ping": 700.0, "decay": 0.09, "volume": 0.8},
    "red": {"click": 0.2, "ping": 250.0, "decay": 0.07, "volume": 0.6},
    "black": {"click": 0.3, "ping": 200.0, "decay": 0.08, "volume": 0.7},
}


def load_config(path: Path | str | None = None) -> Dict[str, Any]:
    """
    Yapılandırmayı config.json'dan yükler. Dosya yoksa varsayılanları
    döndürür ve dosyayı oluşturur.
    """
    config_path = Path(path) if path is not None else CONFIG_PATH
    cfg: Dict[str, Any] = dict(DEFAULTS)

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            if isinstance(user_cfg, dict):
                cfg.update(user_cfg)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[UYARI] config.json okunamadı, varsayılan kullanılıyor: {exc}")
    else:
        save_config(cfg, config_path)

    return cfg


def save_config(cfg: Dict[str, Any], path: Path | str | None = None) -> None:
    """Yapılandırmayı config.json dosyasına yazar."""
    config_path = Path(path) if path is not None else CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"[HATA] config.json yazılamadı: {exc}")


def get_switch_preset(switch: str) -> Dict[str, float]:
    """Belirtilen anahtar çifti türü için preset değerlerini döndürür."""
    preset = SWITCH_PRESETS.get(switch.lower())
    if preset is None:
        print(f"[UYARI] Bilinmeyen switch türü '{switch}', 'blue' kullanılıyor.")
        preset = SWITCH_PRESETS["blue"]
    return dict(preset)
