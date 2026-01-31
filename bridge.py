import os
import socket
import time
from meshtastic.serial_interface import SerialInterface
from pubsub import pub

SOCKET_PATH = "/tmp/meshtastic.sock"

# удалить старый сокет, если остался
try:
    os.unlink(SOCKET_PATH)
except FileNotFoundError:
    pass

# поднять unix socket сервер
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print("Waiting for client to connect to socket...")
conn, _ = server.accept()
print("Client connected.")

# подключение к Meshtastic
iface = SerialInterface("/dev/ttyUSB0")
print("Meshtastic interface ready")

def on_receive(packet, interface):
    decoded = packet.get("decoded", {})

    """
    if "position" in decoded:
        pos = decoded["position"]
        lat = pos.get("latitude")
        lon = pos.get("longitude")
        ts  = pos.get("time", int(time.time()))

        if lat is not None and lon is not None:
            line = f"POS {lat} {lon} {ts}\n"
            try:
                conn.sendall(line.encode())
            except BrokenPipeError:
                print("Socket client disconnected")
    """

    if "text" in decoded:
        text = decoded["text"]
        line = f"MSG {text}\n"
        try:
            conn.sendall(line.encode())
        except BrokenPipeError:
            print("Socket client disconnected")

# ВАЖНО: подписка через pubsub
pub.subscribe(on_receive, "meshtastic.receive")

print("Bridge running.")
while True:
    time.sleep(1)
