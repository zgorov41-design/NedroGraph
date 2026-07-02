#!/bin/bash
VENV_DIR="venv"
echo "Проверяем наличие виртуального окружения..."
echo "Checking for a virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Создаём виртуальное окружение..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Ошибка: не удалось создать виртуальное окружение."
        echo "Убедитесь, что установлен python3-full."
        echo "Error: failed to create a virtual environment."
        echo "Make sure that python3-full is installed."
        exit 1
    fi
fi
echo "Активируем виртуальное окружение..."
echo "Activating the virtual environment..."
source "$VENV_DIR/bin/activate"
if ! command -v pip &> /dev/null; then
    echo "Ошибка: pip не найден в виртуальном окружении."
    echo "Error: pip was not found in the virtual environment."
    exit 1
fi
echo "Устанавливаем зависимости..."
echo "Installing dependencies..."
pip install \
    Flask==2.3.3 \
    Werkzeug==2.3.7 \
    Flask-SocketIO==5.3.6 \
    gevent==24.2.1 \
    gevent-websocket==0.10.1
if [ $? -ne 0 ]; then
    echo "Ошибка при установке зависимостей."
    echo "Error installing dependencies."
    exit 1
fi
echo "###Все зависимости установлены###"
echo "Нажмите Enter для выхода..."
echo "###All dependencies are installed###"
echo "Press Enter to exit..."
read
