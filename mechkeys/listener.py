#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listener.py — mechkeys tuş dinleyicisi.

pynput.keyboard.Listener kullanarak klavyedeki tuş basımlarını dinler ve
her basışta uygun mekanik klavye sesini çalar. Tüm işlem yereldir,
hiçbir tuş verisi dışarıya gönderilmez.

Not: Linux/X11'de pynput bir X sunucusuna ihtiyaç duyar (DISPLAY değişkeni).
Başlıksız/headless ortamdaMockListener kullanılabilir.
"""

from __future__ import annotations

from typing import Callable, Optional

try:
    from pynput.keyboard import Key, Listener  # type: ignore
    _HAS_PYNPUT = True
except Exception:  # pragma: no cover - pynput yoksa mock kullanılır
    _HAS_PYNPUT = False
    Key = None  # type: ignore[assignment]

# Tuş kategorileri (pynput yoksa boş)
MODIFIER_KEYS = set()
if Key is not None:
    MODIFIER_KEYS = {
        Key.shift, Key.shift_l, Key.shift_r,
        Key.ctrl, Key.ctrl_l, Key.ctrl_r,
        Key.alt, Key.alt_l, Key.alt_r,
        Key.cmd, Key.cmd_l, Key.cmd_r,
        Key.alt_gr,
    }


class KeyListener:
    """Tuş dinleyici yöneticisi."""

    def __init__(
        self,
        on_press: Callable[[object], None],
        on_release: Optional[Callable[[object], None]] = None,
    ) -> None:
        self.on_press = on_press
        self.on_release = on_release
        self._listener: Optional[Listener] = None
        self._running = False

    def start(self) -> bool:
        """Dinleyiciyi başlatır. Başarılıysa True döndürür."""
        if not _HAS_PYNPUT:
            print("[HATA] pynput kurulu değil. 'pip install pynput' çalıştırın.")
            return False
        if self._running:
            return True
        try:
            self._listener = Listener(
                on_press=self._wrap_press,
                on_release=self._wrap_release,
            )
            self._listener.start()
            self._running = True
            return True
        except Exception as exc:
            print(f"[HATA] Tuş dinleyici başlatılamadı: {exc}")
            return False

    def stop(self) -> None:
        """Dinleyiciyi durdurur."""
        if self._listener is not None:
            try:
                self._listener.stop()
            except Exception:
                pass
        self._listener = None
        self._running = False

    def join(self) -> None:
        """Dinleyici bitene kadar bekler."""
        if self._listener is not None:
            try:
                self._listener.join()
            except Exception:
                pass

    def _wrap_press(self, key: object) -> None:
        try:
            self.on_press(key)
        except Exception as exc:
            print(f"[UYARI] on_press hatası: {exc}")

    def _wrap_release(self, key: object) -> None:
        if self.on_release is None:
            return
        try:
            self.on_release(key)
        except Exception as exc:
            print(f"[UYARI] on_release hatası: {exc}")

    @property
    def running(self) -> bool:
        return self._running


class MockListener:
    """Headless / test ortamı için gerçek dinleyici simülasyonu."""

    def __init__(
        self,
        on_press: Callable[[object], None],
        on_release: Optional[Callable[[object], None]] = None,
    ) -> None:
        self.on_press = on_press
        self.on_release = on_release
        self._running = False

    def start(self) -> bool:
        self._running = True
        print("[BILGI] MockListener etkin (gerçek tuş dinlemesi yok).")
        return True

    def stop(self) -> None:
        self._running = False

    def join(self) -> None:
        pass

    @property
    def running(self) -> bool:
        return self._running
