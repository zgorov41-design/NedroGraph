# Импорты
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime
from flask import request
from flask_socketio import join_room, emit
import logging
import signal
import sys

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

MAX_HISTORY_LENGTH = 100
message_history = []

@app.route('/')
def index():
    return render_template('index.html')

# Подключение
@socketio.on('connect')
def handle_connect():
    logger.info(f'Client connected: {request.sid}')

# Отключение
@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f'Client disconnected: {request.sid}')

# Вход в чат
@socketio.on('join_room')
def handle_join_room(data):
    try:
        username = data.get('username', 'Гость')
        room = data.get('room', 'main_chat')

        join_room(room)

        socketio.emit(
            'status',
            {'msg': f'{username} присоединился к чату'},
            room=room
        )

        socketio.emit('message_history', message_history, to=request.sid)
        logger.info(f'{username} успешно вошёл в чат {room}')
    except Exception as e:
        logger.error(f'Ошибка при входе в чат: {e}')

@socketio.on('send_message')
def handle_send_message(data):
    try:
        if not data or 'username' not in data or 'text' not in data:
            logger.warning(f'Получены некорректные данные: {data}')
            return

        username = data['username']
        text = data['text'].strip()

        if not text:
            logger.warning(f'Получена пустая строка от {username}')
            return

        room = data.get('room', 'main_chat')
        timestamp = datetime.now().strftime('%H:%M')

        message = {
            'username': username,
            'text': text,
            'timestamp': timestamp
        }

        message_history.append(message)
        if len(message_history) > MAX_HISTORY_LENGTH:
            message_history.pop(0)
        logger.info(f'Сообщение добавлено в историю: {message}')
        socketio.emit(
            'new_message',
            message,
            room=room
        )
        logger.info(f'Отправляем new_message всем в комнате {room} (включая отправителя)')
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения: {e}')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    logger.info(f"Получен сигнал {signum} — остановка сервера...")
    sys.exit(0)

# Обработчики сигналов
signal.signal(signal.SIGINT, signal_handler) 
signal.signal(signal.SIGTERM, signal_handler) 

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    debug_mode = False

    logger.info(f"🚀 Запуск мессенджера на http://{host}:{port}")
    try:
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug_mode
        )
    except Exception as e:
        logger.error(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == '__main__':
    logger.info("Запуск сервера на http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
