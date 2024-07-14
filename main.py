import socket
from threading import Thread
from packets.player_identification import handle_player_identification
from packets.server_identification import create_server_identification_packet
from packets.level_initialize import create_level_initialize_packet
from packets.level_data_chunk import create_level_data_chunk_packet
from packets.level_finalize import create_level_finalize_packet
from client_manager import Client, send_ping, add_client, remove_client
from packets.set_block_client import handle_set_block_packet as handle_client_set_block
from packets.set_block_server import create_set_block_packet as create_server_set_block
from world import get_compressed_level_data, get_level_dimensions, save_world, load_world, set_block, send_level_to_client

# Параметры сервера
HOST = 'localhost'
PORT = 25565

# Параметры идентификации сервера
PROTOCOL_VERSION = 0x07
SERVER_NAME = "Greentea server"
SERVER_MOTD = "Welcome to the server!"
USER_TYPE = 0x00  # 0x64 для оператора сервера, 0x00 для обычного игрока

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

print(f"Сервер запущен на {HOST}:{PORT}")

def broadcast_packet(packet, except_client=None):
    for client in clients:
        if client != except_client:
            with client.lock:
                client.socket.sendall(packet)

# Загрузка мира при запуске сервера
load_world()

def handle_client(client_socket):
    client = Client(client_socket)
    try:
        # Получаем данные от клиента
        data = client.socket.recv(1024)
        
        # Обрабатываем пакет идентификации игрока
        try:
            player_info = handle_player_identification(data)
            print(f"Получен пакет идентификации игрока:")
            for key, value in player_info.items():
                print(f"  {key}: {value}")
            
            # Формируем и отправляем пакет идентификации сервера
            server_packet = create_server_identification_packet(
                PROTOCOL_VERSION, SERVER_NAME, SERVER_MOTD, USER_TYPE
            )
            with client.lock:
                client.socket.sendall(server_packet)
            print("Пакет идентификации сервера отправлен клиенту.")
            
            # Отправляем уровень клиенту
            send_level_to_client(client)
            
            # Добавляем клиента в общий список
            add_client(client)
            clients.append(client)
            
            # Цикл ожидания сообщений от клиента
            while True:
                try:
                    data = client.socket.recv(1024)
                    if not data:
                        break
                    
                    # Обрабатываем пакет установки блока от клиента
                    try:
                        block_info = handle_client_set_block(data)
                        print(f"Пакет установки блока от клиента: {block_info}")
                        
                        # Если режим 0x00, то блок уничтожается
                        if block_info['mode'] == 0x00:
                            block_type = 0  # Тип блока 0 означает, что блок уничтожен
                        else:
                            block_type = block_info['block_type']
                        
                        # Обновляем блок в мире
                        set_block(block_info['x'], block_info['y'], block_info['z'], block_type)
                        save_world()  # Сохраняем мир после изменения
                        
                        # Создаем и рассылаем пакет установки блока от сервера
                        server_set_block_packet = create_server_set_block(
                            block_info['x'], block_info['y'], block_info['z'], block_type
                        )
                        broadcast_packet(server_set_block_packet, except_client=client)
                        print("Пакет установки блока от сервера разослан всем клиентам.")
                        
                    except ValueError as e:
                        print(f"Ошибка при обработке пакета установки блока: {e}")
                    
                except Exception as e:
                    print(f"Ошибка при получении данных от клиента: {e}")
                    break
            
        except ValueError as e:
            print(f"Ошибка: {e}")
    finally:
        remove_client(client)
        clients.remove(client)

# Запускаем поток для отправки пинг-пакетов всем клиентам
ping_thread = Thread(target=send_ping)
ping_thread.daemon = True  # Завершаем поток при завершении программы
ping_thread.start()
print("Поток для отправки пинг-пакетов всем клиентам запущен.")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Новое подключение от {addr}")
    client_thread = Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
