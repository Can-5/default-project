#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
github-auto-deploy — GitHub otomatik commit + push akışı.
Belirtilen dizindeki değişiklikleri commit'leyip push'lar.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime


def run_cmd(cmd, cwd=None):
    """Komut çalıştırıp çıkış döndürür."""
    result = subprocess.run(cmd, shell=True, cwd=cwd,
                            capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def is_git_repo(path):
    """Verilen dizin git reposu mu kontrol eder."""
    out, _, rc = run_cmd("git rev-parse --is-inside-work-tree", cwd=path)
    return rc == 0 and out == "true"


def has_changes(path):
    """Commitlenmemiş değişiklik var mı kontrol eder."""
    out, _, _ = run_cmd("git status --porcelain", cwd=path)
    return bool(out.strip())


def get_branch(path):
    """Mevcut branch adını döndürür."""
    out, _, _ = run_cmd("git branch --show-current", cwd=path)
    return out


def auto_deploy(path, message=None, branch=None, push=True):
    """Otomatik commit ve push işlemini gerçekleştirir."""
    if not is_git_repo(path):
        print(f"Hata: '{path}' bir git deposu değil.")
        return False

    if not has_changes(path):
        print("Commitlenecek değişiklik yok.")
        return True

    current_branch = get_branch(path)
    target_branch = branch or current_branch
    print(f"Mevcut branch: {current_branch}")
    print(f"Hedef branch: {target_branch}")

    if target_branch != current_branch:
        out, err, rc = run_cmd(f"git checkout {target_branch}", cwd=path)
        if rc != 0:
            print(f"Branch değiştirilemedi: {err}")
            return False

    # Tüm değişiklikleri stage et
    run_cmd("git add -A", cwd=path)

    commit_msg = message or f"auto-deploy: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    out, err, rc = run_cmd(f'git commit -m "{commit_msg}"', cwd=path)
    if rc != 0:
        print(f"Commit başarısız: {err}")
        return False
    print(f"Commit başarılı: {commit_msg}")

    if push:
        out, err, rc = run_cmd(f"git push origin {target_branch}", cwd=path)
        if rc != 0:
            print(f"Push başarısız: {err}")
            return False
        print(f"Push başarılı: origin/{target_branch}")

    return True


def main():
    parser = argparse.ArgumentParser(description="GitHub otomatik deploy")
    parser.add_argument("path", help="Git reposu dizin yolu")
    parser.add_argument("-m", "--message", help="Commit mesajı")
    parser.add_argument("-b", "--branch", help="Hedef branch")
    parser.add_argument("--no-push", action="store_true",
                        help="Sadece commit et, push yapma")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Hata: '{args.path}' dizin bulunamadı.")
        sys.exit(1)

    success = auto_deploy(
        args.path,
        message=args.message,
        branch=args.branch,
        push=not args.no_push,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
