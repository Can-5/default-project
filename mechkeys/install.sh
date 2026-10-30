#!/usr/bin/env bash
# install.sh — mechkeys masaüstü uygulamasını CakyOS/Linux'a kurar.
# Çalıştırma: ./install.sh   (mechkeys/ dizininde)
set -euo pipefail

APP_DIR="$HOME/.local/share/mechkeys"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
BIN_DIR="$HOME/.local/bin"

echo "[1/4] Dizinler oluşturuluyor..."
mkdir -p "$APP_DIR" "$DESKTOP_DIR" "$AUTOSTART_DIR" "$BIN_DIR"

echo "[2/4] Uygulama dosyaları kopyalanıyor..."
cp -r "$(dirname "$0")"/* "$APP_DIR/"
chmod +x "$APP_DIR/mechkeys" "$APP_DIR/mechkeys.py"

echo "[3/4] Uygulama menüsü kısayolu..."
sed "s|/home/ilkaycan/.local/share/mechkeys|$APP_DIR|g" \
    "$APP_DIR/mechkeys.desktop" > "$DESKTOP_DIR/mechkeys.desktop"
chmod +x "$DESKTOP_DIR/mechkeys.desktop"

echo "[4/4] Oturum başlangıcına ekleniyor..."
cp "$DESKTOP_DIR/mechkeys.desktop" "$AUTOSTART_DIR/mechkeys.desktop"
chmod +x "$AUTOSTART_DIR/mechkeys.desktop"

# PATH'e ~/.local/bin eklemek için ipucu
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo ""
    echo "IPUÇU: ~/.local/bin PATH'inizde değil. .bashrc'yanıza ekleyin:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "Tamam. MechKeys uygulama menüsünde 'MechKeys' olarak görünür ve"
echo "oturum açışında otomatik başlar. Kaldırmak için:"
echo "  rm $DESKTOP_DIR/mechkeys.desktop $AUTOSTART_DIR/mechkeys.desktop"
echo "  rm -rf $APP_DIR"
