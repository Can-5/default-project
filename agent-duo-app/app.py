#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""app.py — agent-duo-app ana giriş noktası."""

from duo import run_duo


def main():
    import argparse
    parser = argparse.ArgumentParser(description="2 ajanın kullanabileceği kod inceleme uygulaması")
    parser.add_argument("--target", required=True, help="Hedef dosya yolu")
    parser.add_argument("--json", action="store_true", help="JSON çıkış")
    parser.add_argument("--out", default="reports", help="Rapor dizini")
    args = parser.parse_args()

    run_duo(args.target) if False else None
    # duo.main'i çağır
    from duo import main as duo_main
    # argparse çakışmasını önlemek için duo.main'e geçir
    import sys
    sys.argv = ["duo", "--target", args.target]
    if args.json:
        sys.argv.append("--json")
    if args.out != "reports":
        sys.argv += ["--out", args.out]
    duo_main()


if __name__ == "__main__":
    main()