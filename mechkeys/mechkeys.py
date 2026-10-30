#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mechkeys.py — mechkeys masaüstü uygulaması ana girişi.

Klavyedeki her tuş basışında mekanik klavye sesi çalar. Pure-Python
ses sentezi (harici ses dosyası gerekmez) + pynput tuş dinleyici +
birden fazla ses arka ucu. Tüm işlem yereldir, telemetri yok.

Kullanım:
    python3 mechkeys.py                    # varsayılan (mavi switch, ses aç)
    python3 mechkeys.py --switch brown     # mavi dışında bir switch türü
    python3 mechkeys.py --volume 0.5       # ses seviyesi
    python3 mechkeys.py --test             # tek bir test sesi çalar
    python3 mechkeys.py --no-audio         # dinleme yapar, ses yok (log)
    python3 mechkeys.py --backend paplay   # zorunlu ses arka ucu

Çıkış: CTRL+C
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

# Yerel modüller
from config import DEFAULTS, get_switch_preset, load_config, save_config
from audio import AudioPlayer, synthesize_click, synthesize_spacebar
from listener import KeyListener, MockListener, _HAS_PYNPUT

__version__ = "1.0.0"


class MechKeys:
    """mechkeys uygulaması: dinleyici + ses motoru birleşimi."""

    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.switch: str = str(cfg.get("switch", DEFAULTS["switch"]))
        self.volume: float = float(cfg.get("volume", DEFAULTS["volume"]))
        self.enabled: bool = bool(cfg.get("enabled", DEFAULTS["enabled"]))
        self.modifiers_silent: bool = bool(
            cfg.get("modifiers_silent", DEFAULTS["modifiers_silent"])
        )
        self.spacebar_louder: bool = bool(
            cfg.get("spacebar_louder", DEFAULTS["spacebar_louder"])
        )
        self.backend: str = str(cfg.get("audio_backend", DEFAULTS["audio_backend"]))
        self.toggle_hotkey: str = str(cfg.get("toggle_hotkey", DEFAULTS["toggle_hotkey"]))

        self.player = AudioPlayer(
            backend=self.backend,
            volume=self.volume,
            sample_rate=int(cfg.get("sample_rate", DEFAULTS["sample_rate"])),
        )

        self._press_count = 0

    def _key_name(self, key) -> str:
        """Tuşun okunabilir adını döndürür (log/debug için)."""
        try:
            return key.char  # type: ignore[attr-defined]
        except AttributeError:
            return str(key).replace("Key.", "")

    def _is_modifier(self, key) -> bool:
        from listener import MODIFIER_KEYS  # local import
        return key in MODIFIER_KEYS

    def _is_toggle(self, key) -> bool:
        """Toggle kısayol tuşuna basılmış mı?"""
        try:
            return str(key).lower().replace("key.", "") == self.toggle_hotkey.lower()
        except Exception:
            return False

    def on_press(self, key) -> None:
        """Her tuş basışında çağrılır."""
        if self._is_toggle(key):
            self.enabled = not self.enabled
            state = "açık" if self.enabled else "kapalı"
            print(f"[mechkeys] ses {state} (kısayol: {self.toggle_hotkey})")
            return

        if not self.enabled:
            return

        if self.modifiers_silent and self._is_modifier(key):
            return

        name = self._key_name(key)
        loud = self.spacebar_louder and name == "space"

        self._press_count += 1
        print(f"[{self._press_count}] tuş: {name}  switch: {self.switch} "
              f"{'(boşluk)' if loud else ''}")

        if loud:
            self.player.play_click(switch=self.switch, loud=True)
        else:
            self.player.play_click(switch=self.switch)

    def run(self, mock: bool = False) -> int:
        """Uygulamayı çalıştırır. CTRL+C ile durur."""
        ListenerCls = MockListener if mock else KeyListener
        listener = ListenerCls(on_press=self.on_press)

        if not listener.start():
            if not mock and _HAS_PYNPUT:
                print("[BILGI] X11 ekranı bulunamadı, mock moda geçiliyor.")
                listener = MockListener(on_press=self.on_press)
                listener.start()
            else:
                return 1

        print("=" * 55)
        print(f" mechkeys v{__version__} çalışıyor")
        print(f" switch: {self.switch} | ses: {'açık' if self.enabled else 'kapalı'}")
        print(f" arka uç: {self.player._selected or self.backend}")
        print(f" toggle: {self.toggle_hotkey} | çıkış: CTRL+C")
        print("=" * 55)

        try:
            while listener.running:
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\n[mechkeys] durduruluyor...")
        finally:
            listener.stop()
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mechkeys",
        description="Mekanik klavye ses simülatörü (tuş dinleyici).",
    )
    parser.add_argument("--version", action="version", version=f"mechkeys {__version__}")
    parser.add_argument(
        "--switch",
        choices=["blue", "brown", "red", "black"],
        default=None,
        help="Anahtar çifti türü (varsayılan: blue / config.json)",
    )
    parser.add_argument(
        "--volume",
        type=float,
        default=None,
        help="Ses seviyesi 0.0 - 1.0 (varsayılan: 0.7 / config.json)",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "pygame", "paplay", "aplay", "ffplay", "silent"],
        default=None,
        help="Ses arka ucu (varsayılan: auto / config.json)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Tek bir test sesi çalar ve çıkar (dinlemez).",
    )
    parser.add_argument(
        "--no-audio",
        action="store_true",
        help="Tuşları dinler ama ses çıkarmıyor (sadece log).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Gerçek dinleyici yerine mock listener kullanır (test).",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Özel config.json yolu (varsayılan: mechkeys/config.json)",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config_path = Path(args.config) if args.config else None
    cfg = load_config(config_path)

    # CLI argümanları config'i geçersiz kılar
    if args.switch is not None:
        cfg["switch"] = args.switch
    if args.volume is not None:
        cfg["volume"] = max(0.0, min(1.0, args.volume))
    if args.backend is not None:
        cfg["audio_backend"] = args.backend
    if args.no_audio:
        cfg["enabled"] = False
        cfg["audio_backend"] = "silent"

    # Değişiklikleri kalıcı yap (switch/volume/backend)
    save_config(cfg, config_path)

    app = MechKeys(cfg)

    if args.test:
        print(f"[mechkeys] test sesi (switch={app.switch}, volume={app.volume})")
        app.player.play_click(switch=app.switch)
        app.player.play_click(switch=app.switch, loud=True)
        print("[mechkeys] test tamamlandı.")
        return 0

    return app.run(mock=args.mock)


if __name__ == "__main__":
    sys.exit(main())
