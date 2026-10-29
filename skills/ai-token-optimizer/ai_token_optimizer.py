#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-token-optimizer — Yapay zeka token tüketimini analiz eder ve optimize eder.
İstemleri (prompt) inceleyerek gereksiz token'ları azaltır, bütçe yönetimi ve verimlilik ipuçları sağlar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
USAGE_FILE = DATA_DIR / "token_usage.json"


def count_tokens(text: str) -> int:
    """Yaklaşık token sayısını hesaplar (karekter / 4)."""
    return max(1, len(text) // 4)


def analyze_prompt(text: str) -> dict:
    """İstem metnini analiz eder ve istatistikleri döndürür."""
    total_chars = len(text)
    total_tokens = count_tokens(text)
    words = len(text.split())
    lines = text.count("\n") + 1
    repeats = len(re.findall(r"(.)\1{3,}", text))
    filler_words = [
        "very", "really", "just", "quite", "basically", "actually",
        "sadece", "pek", "basitçe", "gereksiz", "çok",
    ]
    filler_count = sum(len(re.findall(rf"\b{w}\b", text, re.IGNORECASE)) for w in filler_words)

    return {
        "chars": total_chars,
        "tokens": total_tokens,
        "words": words,
        "lines": lines,
        "repeats": repeats,
        "filler_words": filler_count,
    }


def optimize_text(text: str) -> str:
    """İstem metnini optimize eder (gereksiz boşlukları temizler, tekrarlanan satırları birleştirir)."""
    optimized = re.sub(r"\s+", " ", text)
    optimized = re.sub(r"\n\s*\n+", "\n", optimized)
    return optimized.strip()


def load_tips() -> list:
    """Token tasarruf ipuçlarını döndürür."""
    return [
        "İstemde gereksiz sıfatlardan kaçının.",
        "Sistem mesajını kısa ve net tutun.",
        "Örnek verilerde gereksiz detayları çıkarın.",
        "Tekrar eden cümleleri birleştirin.",
        "Context'i düzenli olarak temizleyin.",
        "Kısa ve öz komutlar kullanın.",
        "Gereksiz açıklamaları çıkarın.",
        "Tek seferde çok fazla görev vermeyin.",
        "Token bütçesi belirleyip ona göre çalışın.",
        "Gereksiz metinleri kısaltın.",
    ]


def main():
    parser = argparse.ArgumentParser(description="AI Token Optimizer")
    parser.add_argument("--analyze", metavar="FILE", help="İstem dosyasını analiz et")
    parser.add_argument("--optimize", metavar="FILE", help="İstem dosyasını optimize et")
    parser.add_argument("--output", metavar="FILE", help="Çıkış dosyası")
    parser.add_argument("--tips", action="store_true", help="Token tasarruf ipuçlarını göster")
    args = parser.parse_args()

    if args.tips:
        tips = load_tips()
        print("=== Token Tasarruf İpuçları ===")
        for i, tip in enumerate(tips, 1):
            print(f"{i}. {tip}")
        return

    if args.analyze:
        path = Path(args.analyze)
        if not path.exists():
            print(f"Hata: Dosya bulunamadı: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        stats = analyze_prompt(text)
        print(f"=== İstem Analizi: {path} ===")
        print(f"Karakter: {stats['chars']}")
        print(f"Yaklaşık Token: {stats['tokens']}")
        print(f"Kelime: {stats['words']}")
        print(f"Satır: {stats['lines']}")
        print(f"Tekrarlayan Karakter: {stats['repeats']}")
        print(f"Doldurma Kelimesi: {stats['filler_words']}")
        if args.output:
            out = Path(args.output)
            out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\nSonuç kaydedildi: {out}")
        return

    if args.optimize:
        path = Path(args.optimize)
        if not path.exists():
            print(f"Hata: Dosya bulunamadı: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        stats = analyze_prompt(text)
        optimized = optimize_text(text)
        out_stats = analyze_prompt(optimized)
        print(f"=== Optimizasyon: {path} ===")
        print(f"Önce: {stats['tokens']} token → Sonra: {out_stats['tokens']} token")
        print(f"Tasarruf: {stats['tokens'] - out_stats['tokens']} token")
        if args.output:
            out = Path(args.output)
            out.write_text(optimized, encoding="utf-8")
            print(f"Optimize metin kaydedildi: {out}")
        else:
            print("\n--- Optimize İstemi ---")
            print(optimized)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
