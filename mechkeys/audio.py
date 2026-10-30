#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio.py — mechkeys ses motoru.

Pure-Python (wave/math/struct) ile mekanik klavye sesi sentezler ve
birden fazla arka uçla oynatır. Harici ses dosyası gerektirmez.

Desteklenen arka uçlar:
  * pygame.mixer   — en iyi Python ses desteği (isteğe bağlı bağımlılık)
  * paplay         — PulseAudio (Linux'ta çoğunlukla kurulu)
  * aplay          — ALSA (Linux'ta çoğunlukla kurulu)
  * ffplay         — FFmpeg (isteğe bağlı)
  * silent         — sessiz mod (test / başlıksız ortam)

Arka uç 'auto' ise mevcut olan ilk çalışan arka uç seçilir.
"""

from __future__ import annotations

import math
import struct
import subprocess
import sys
import wave
from io import BytesIO
from pathlib import Path
from typing import Dict, Optional

try:  # pygame opsiyonel
    import pygame  # type: ignore
    _HAS_PYGAME = True
except Exception:  # pragma: no cover
    _HAS_PYGAME = False


def _sine(freq: float, duration: float, sample_rate: int) -> list[float]:
    """Belirtilen frekansta bir sinus dalgası döndürür (-1.0 .. 1.0)."""
    count = int(sample_rate * duration)
    return [math.sin(2.0 * math.pi * freq * i / sample_rate) for i in range(count)]


def _noise(duration: float, sample_rate: int, seed: int = 42) -> list[float]:
    """Beyaz gürültü (white noise) döndürür (-1.0 .. 1.0)."""
    import random

    rng = random.Random(seed)
    count = int(sample_rate * duration)
    return [rng.uniform(-1.0, 1.0) for _ in range(count)]


def _envelope_attack_decay(length: int, attack: float, decay: float) -> list[float]:
    """Hızlı saldırı, yavaş çalan envelop (0.0 .. 1.0)."""
    env = []
    for i in range(length):
        t = i / max(1, length - 1)
        if t < attack:
            env.append(t / max(attack, 1e-6))
        else:
            env.append(math.exp(-(t - attack) / max(decay, 1e-6)))
    return env


def synthesize_click(
    switch: str = "blue",
    volume: float = 0.7,
    sample_rate: int = 44100,
) -> bytes:
    """
    Mekanik klavye tuş sesini WAV formatında bytes olarak üretir.

    Bileşenler:
      * 'click'  — kısa beyaz gürültü patlaması (tuşun quelalinğı)
      * 'ping'   — kısa sinus tonu (anahtar çifti frekansı)
    İkisi bir hızlı saldırı/çalan envelop ile birleştirilir.
    """
    presets: dict[str, dict[str, float]] = {
        "blue": {"click": 0.9, "ping": 1000.0, "decay": 0.12, "vol": 1.0},
        "brown": {"click": 0.5, "ping": 700.0, "decay": 0.09, "vol": 0.8},
        "red": {"click": 0.2, "ping": 250.0, "decay": 0.07, "vol": 0.6},
        "black": {"click": 0.3, "ping": 200.0, "decay": 0.08, "vol": 0.7},
    }
    p = presets.get(switch.lower(), presets["blue"])

    dur = 0.16  # toplam süre (saniye)
    n = int(sample_rate * dur)
    attack = 0.004
    decay = p["decay"]
    env = _envelope_attack_decay(n, attack, decay)

    # Click bileşeni: kısa beyaz gürültü patlaması (tuşun quelalinğı)
    click_env = _envelope_attack_decay(n, 0.002, 0.05)
    noise = _noise(dur, sample_rate)
    click = [x * click_env[i] * p["click"] for i, x in enumerate(noise)]

    # Ping bileşeni: kısa sinus tonu (anahtar çifti frekansı)
    ping = _sine(p["ping"], dur, sample_rate)
    ping = [x * env[i] * p["vol"] * 0.6 for i, x in enumerate(ping)]

    # Birleştir, normalize et ve ses seviyesine göre ölçekle
    mixed = [click[i] + ping[i] for i in range(n)]
    peak = max(abs(x) for x in mixed) or 1.0
    mixed = [x / peak * 0.9 * volume for x in mixed]

    # 16-bit PCM WAV'a dönüştür
    frames = bytearray()
    for x in mixed:
        val = int(max(-1.0, min(1.0, x)) * 32767)
        frames += struct.pack("<h", val)

    buf = BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)           # mono
        w.setsampwidth(2)           # 16-bit
        w.setframerate(sample_rate)
        w.writeframes(bytes(frames))
    return buf.getvalue()


def synthesize_spacebar(volume: float = 0.7, sample_rate: int = 44100) -> bytes:
    """Boşluk tuşu için daha uzun, daha ağır bir ses."""
    preset_click = 1.0
    preset_ping = 400.0
    preset_decay = 0.15
    dur = 0.22
    n = int(sample_rate * dur)
    env = _envelope_attack_decay(n, 0.005, preset_decay)
    noise = _noise(dur, sample_rate)
    click = [x * env[i] * preset_click * 0.5 for i, x in enumerate(noise)]
    ping = _sine(preset_ping, dur, sample_rate)
    ping = [x * env[i] * 0.5 for i, x in enumerate(ping)]
    mixed = [click[i] + ping[i] for i in range(n)]
    peak = max(abs(x) for x in mixed) or 1.0
    mixed = [x / peak * 0.9 * volume for x in mixed]
    frames = bytearray()
    for x in mixed:
        val = int(max(-1.0, min(1.0, x)) * 32767)
        frames += struct.pack("<h", val)
    buf = BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(bytes(frames))
    return buf.getvalue()


class AudioPlayer:
    """Ses oynatıcı. Birden fazla arka ucu dene, ilk çalışanı kullan."""

    def __init__(
        self,
        backend: str = "auto",
        volume: float = 0.7,
        sample_rate: int = 44100,
    ) -> None:
        self.backend = backend
        self.volume = max(0.0, min(1.0, volume))
        self.sample_rate = sample_rate
        self._selected: Optional[str] = None
        self._pygame_mixer = None
        self._init_backend()

    def _init_backend(self) -> None:
        order: list[str]
        if self.backend == "auto":
            order = ["pygame", "paplay", "aplay", "ffplay", "silent"]
        elif self.backend == "silent":
            order = ["silent"]
        else:
            order = [self.backend]

        for name in order:
            if self._try(name):
                self._selected = name
                print(f"[mechkeys] ses arka ucu: {name}")
                return
        self._selected = "silent"
        print("[mechkeys] ses arka ucu: silent (ses yok)")

    def _try(self, name: str) -> bool:
        if name == "pygame":
            if not _HAS_PYGAME:
                return False
            try:
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1)
                self._pygame_mixer = pygame.mixer
                return True
            except Exception:
                return False
        if name in ("paplay", "aplay", "ffplay"):
            return subprocess.run(["which", name],
                                  capture_output=True).returncode == 0
        if name == "silent":
            return True
        return False

    def play_bytes(self, wav_bytes: bytes) -> None:
        """WAV bytes'ını seçilen arka uçla oynatır (bloke etmez)."""
        if self._selected == "silent":
            return
        if self._selected == "pygame" and self._pygame_mixer is not None:
            self._play_pygame(wav_bytes)
        elif self._selected in ("paplay", "aplay", "ffplay"):
            self._play_subprocess(self._selected, wav_bytes)

    def _play_pygame(self, wav_bytes: bytes) -> None:
        try:
            sound = self._pygame_mixer.Sound(buffer=wav_bytes)
            sound.set_volume(self.volume)
            sound.play()
        except Exception as exc:
            print(f"[UYARI] pygame oynatma hatası: {exc}")

    def _play_subprocess(self, cmd: str, wav_bytes: bytes) -> None:
        try:
            subprocess.Popen(
                [cmd, "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).communicate(input=wav_bytes, timeout=5)
        except Exception as exc:
            print(f"[UYARI] {cmd} oynatma hatası: {exc}")

    def play_click(self, switch: str = "blue", loud: bool = False) -> None:
        """Mekanik klavye tık sesini oynatır."""
        if loud:
            wav = synthesize_spacebar(volume=self.volume, sample_rate=self.sample_rate)
        else:
            wav = synthesize_click(switch=switch, volume=self.volume,
                                   sample_rate=self.sample_rate)
        self.play_bytes(wav)
