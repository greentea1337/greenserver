import time
from threading import Lock, Thread

# Список для хранения всех подключенных клиентов и их сокетов
clients = []
clients_lock = Lock()

class Client:
    def __init__(self, socket):
        self.socket = socket
        self.lock = Lock()

def create_ping_packet():
    packet_id = 0x01
    return bytes([packet_id])

def send_ping():
    while True:
        time.sleep(10)  # Отправляем пакет Ping каждые 10 секунд
        with clients_lock:
            for client in clients:
                try:
                    ping_packet = create_ping_packet()
                    with client.lock:
                        client.socket.sendall(ping_packet)
                    print("Пакет Ping отправлен клиенту.")
                except Exception as e:
                    print(f"Ошибка при отправке пинг-пакета: {e}")
                    clients.remove(client)
                    client.socket.close()

# Функция для добавления клиента в список
def add_client(client):
    with clients_lock:
        clients.append(client)
    print("Клиент добавлен в общий список.")

# Функция для удаления клиента из списка
def remove_client(client):
    with clients_lock:
        if client in clients:
            clients.remove(client)
    client.socket.close()
    print("Клиент отключился и был удален из списка.")