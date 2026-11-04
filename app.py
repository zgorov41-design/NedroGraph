from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime
from flask import request
from flask_socketio import join_room, emit
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

message_history = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f'Client disconnected: {request.sid}')

@socketio.on('join_room')
def handle_join_room(data):
    username = data.get('username', 'Гость')
    room = data.get('room', 'main_chat')

    join_room(room)

    emit('status', {
        'msg': f'{username} присоединился к чату'
    }, room=room)

    emit('message_history', message_history.get(room, []), to=request.sid)

    logger.info(f'{username} вошёл в чат {room}')

@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username')
    text = data.get('text', '').strip()
    room = data.get('room', 'main_chat')

    if not username or not text:
        return

    message = {
        'username': username,
        'text': text,
        'timestamp': datetime.now().strftime('%H:%M')
    }

    message_history.setdefault(room, []).append(message)

    socketio.emit('new_message', message, room=room)

def signal_handler(signum, frame):
    logger.info(f"Получен сигнал {signum} — остановка сервера...")
    sys.exit(0)

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