#!/bin/bash
source venv/bin/activate
APP_DIR=$(find ~ -type d -name "messenger" | head -1)
if [ -z "$APP_DIR" ]; then
    echo "❌ Директория 'messenger' не найдена в домашней директории"
    echo "❌ The 'messenger' directory was not found in the home directory"
    exit 1
fi
if [ ! -f "$APP_DIR/app.py" ]; then
    echo "❌ Файл app.py не найден в директории: $APP_DIR"
    echo "❌ File app.py not found in the directory: $APP_DIR"
    exit 1
fi
echo "🚀 Запускаем: python3 $APP_DIR/app.py"
echo "🚀 Launching: python3 $APP_DIR/app.py "
echo "Нажмите Ctrl+C для остановки"
echo "Press Ctrl+C to stop"
python3 "$APP_DIR/app.py"
echo "Нажмите Enter для закрытия терминала..."
echo "Press Enter to close the terminal..."
read
