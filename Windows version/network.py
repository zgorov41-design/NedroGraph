import socketio

logs = False

sio = socketio.Client(logger=logs, engineio_logger=logs)

messages = []

@sio.event
def connect():
    if logs:
        print("✅Connect")

@sio.event
def disconnect():
    if logs:
        print("❌Disconnect")

@sio.on("status")
def receive_status(data):
    if logs:
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
        if logs:
            print("🔌Conect to:", ip)
        sio.connect(
            f"http://{ip}:5000"
        )
        sio.emit(
            "join_room",
            {
                "username": username,
                "room": "main_chat"
            }
        )
        return True
        
    except Exception as e:
            if logs:
                print("❌Error connect:", e)
            return False


def send_message(username, text):
    if not sio.connected:
        if logs:
            print("⛔No connect")
        return
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
