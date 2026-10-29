# Linux Control — OpenCode İçin Linux Komut Kontrolü

## Kurulum

1. `bridge_host.py`'yi gerçek CakyOS masaüstü terminalinde başlatın:
   ```bash
   cd /home/ilkaycan/Belgeler/Default Project/linux-bridge
   python3 bridge_host.py
   ```

2. OpenCode'da `linux-control` skill'ini kullanın:
   ```bash
   python3 skills/linux-control/linux_control.py --shell "whoami"
   python3 skills/linux-control/linux_control.py --browser firefox
   python3 skills/linux-control/linux_control.py --screenshot masaustu.png
   ```

## Örnek Akış

```
Terminal 1 (gerçek CakyOS masaüstü):
  $ python3 bridge_host.py
  [linux-bridge] Host işleyici başlatıldı: ...
  [linux-bridge] İzlenen dizin: .../cmd/

Terminal 2 (OpenCode sandbox):
  $ python3 skills/linux-control/linux_control.py --shell "pacman -Q | wc -l"
  === Shell Çıktısı ===
  1234
```

## Güvenlik Notu

`bridge_host.py` sadece 127.0.0.1 / yerel erişim için tasarlanmıştır. Ağ üzerinden açık değildir.