import socketio

sio = socketio.Client(logger=True, engineio_logger=True)

messages = []

@sio.event
def connect():
    print("✅Connect")

@sio.event
def disconnect():
    print("❌Disconnect")

@sio.on("status")
def receive_status(data):
    print("📊STATUS:", data)

@sio.on("message_history")
def receive_history(data):

    messages.clear()
    messages.extend(data)

@sio.on("new_message")
def receive_message(data):

    messages.append(data)

def connect_to_server(ip, username):
    try:
        print("🔌Conect to:", ip)
        sio.connect(f"http://{ip}:5000")
        print("🟢Connected:", sio.connected)
        sio.emit(
            "join_room",
            {
                "username": username,
                "room": "main_chat"
            }
        )
        return True
    except Exception as e:
        print("❌Error connect:", e)
        return False


def send_message(username, text):
    print("Connected:", sio.connected)
    if not sio.connected:
        print("⛔No connect")
        return
    print("📤Send:", text)
    sio.emit(
        "send_message",
        {
            "username": username,
            "text": text,
            "room": "main_chat"
        }
    )

def get_messages():
    return messages

def disconnect():
    if sio.connected:
        sio.disconnect()
