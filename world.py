import gzip
import struct
import os
import noise
import numpy as np
import random
from packets.level_initialize import create_level_initialize_packet
from packets.level_data_chunk import create_level_data_chunk_packet
from packets.level_finalize import create_level_finalize_packet

# Параметры карты
X_SIZE = 256
Y_SIZE = 64
Z_SIZE = 256
LEVEL_VOLUME = X_SIZE * Y_SIZE * Z_SIZE

# Создаем массив данных уровня
LEVEL_DATA = bytearray(LEVEL_VOLUME)

def generate_perlin_noise(width, depth, scale=50.0, octaves=3, persistence=0.3, lacunarity=2.0):
    noise_data = np.zeros((width, depth))
    seed = random.randint(0, 100)  # Используем случайное значение для seed
    
    for x in range(width):
        for z in range(depth):
            noise_value = noise.pnoise2(
                x / scale,
                z / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=width,
                repeaty=depth,
                base=seed
            )
            # Нормализация шума от диапазона [-1, 1] к [0, 1]
            noise_value = (noise_value + 1) / 2
            noise_data[x][z] = noise_value
                
    return noise_data

def generate_trees():
    tree_count = random.randint(50, 150)  # Генерируем случайное количество деревьев
    for _ in range(tree_count):
        x = random.randint(0, X_SIZE - 1)
        z = random.randint(0, Z_SIZE - 1)
        
        # Ищем высоту земли в данной точке
        for y in range(Y_SIZE-1, -1, -1):
            index = x + (z * X_SIZE) + (y * X_SIZE * Z_SIZE)
            if LEVEL_DATA[index] == 2:  # Если нашли траву
                # Ставим ствол дерева (ID 17)
                tree_height = random.randint(4, 7)  # Случайная высота дерева
                for tree_height_offset in range(tree_height):
                    tree_index = x + (z * X_SIZE) + ((y + tree_height_offset) * X_SIZE * Z_SIZE)
                    LEVEL_DATA[tree_index] = 17
                
                # Ставим листву (ID 18)
                leaf_layers = [
                    (-2, 3), (-1, 4), (0, 5), (1, 4), (2, 3)
                ]
                for dy, size in leaf_layers:
                    for dx in range(-size//2, size//2+1):
                        for dz in range(-size//2, size//2+1):
                            leaf_x = x + dx
                            leaf_y = y + tree_height + dy
                            leaf_z = z + dz
                            if 0 <= leaf_x < X_SIZE and 0 <= leaf_y < Y_SIZE and 0 <= leaf_z < Z_SIZE:
                                leaf_index = leaf_x + (leaf_z * X_SIZE) + (leaf_y * X_SIZE * Z_SIZE)
                                if LEVEL_DATA[leaf_index] == 0:
                                    LEVEL_DATA[leaf_index] = 18
                break

def generate_dandelions():
    dandelion_count = random.randint(200, 400)  # Генерируем случайное количество одуванчиков
    for _ in range(dandelion_count):
        x = random.randint(0, X_SIZE - 1)
        z = random.randint(0, Z_SIZE - 1)
        
        # Ищем высоту земли в данной точке
        for y in range(Y_SIZE-1, -1, -1):
            index = x + (z * X_SIZE) + (y * X_SIZE * Z_SIZE)
            if LEVEL_DATA[index] == 2:  # Если нашли траву
                flower_index = x + (z * X_SIZE) + ((y + 1) * X_SIZE * Z_SIZE)
                if LEVEL_DATA[flower_index] == 0:  # Проверяем, что над травой пустое пространство
                    LEVEL_DATA[flower_index] = 37  # Ставим одуванчик
                break

def generate_roses():
    rose_count = random.randint(50, 100)  # Генерируем случайное количество роз
    for _ in range(rose_count):
        x = random.randint(0, X_SIZE - 1)
        z = random.randint(0, Z_SIZE - 1)
        
        # Ищем высоту земли в данной точке
        for y in range(Y_SIZE-1, -1, -1):
            index = x + (z * X_SIZE) + (y * X_SIZE * Z_SIZE)
            if LEVEL_DATA[index] == 2:  # Если нашли траву
                # Проверяем, что роза растет на определенной высоте (например, выше 32)
                if y > 32:
                    flower_index = x + (z * X_SIZE) + ((y + 1) * X_SIZE * Z_SIZE)
                    if LEVEL_DATA[flower_index] == 0:  # Проверяем, что над травой пустое пространство
                        LEVEL_DATA[flower_index] = 38  # Ставим розу
                break

def generate_flowers():
    generate_dandelions()
    generate_roses()

def initialize_level():
    noise_data = generate_perlin_noise(X_SIZE, Z_SIZE)
    
    for x in range(X_SIZE):
        for z in range(Z_SIZE):
            height = int(noise_data[x][z] * 10) + 32  # Базовая высота 32
            for y in range(Y_SIZE):
                index = x + (z * X_SIZE) + (y * X_SIZE * Z_SIZE)
                if y < height - 4:
                    LEVEL_DATA[index] = 1  # Камень
                elif y < height - 1:
                    LEVEL_DATA[index] = 3  # Земля
                elif y < height:
                    LEVEL_DATA[index] = 2  # Трава
                else:
                    LEVEL_DATA[index] = 0  # Пустота
    generate_trees()
    generate_flowers()

# Инициализируем уровень
initialize_level()

def get_compressed_level_data():
    level_data_with_length = struct.pack('>I', LEVEL_VOLUME) + LEVEL_DATA
    compressed_level_data = gzip.compress(level_data_with_length)
    return compressed_level_data

def get_level_dimensions():
    return X_SIZE, Y_SIZE, Z_SIZE

def save_level_data(filename):
    with gzip.open(filename, 'wb') as f:
        f.write(LEVEL_DATA)

def load_level_data(filename):
    global LEVEL_DATA
    with gzip.open(filename, 'rb') as f:
        LEVEL_DATA = bytearray(f.read())

def set_block(x, y, z, block_type):
    if 0 <= x < X_SIZE and 0 <= y < Y_SIZE and 0 <= z < Z_SIZE:
        index = x + (z * X_SIZE) + (y * X_SIZE * Z_SIZE)
        LEVEL_DATA[index] = block_type
    else:
        raise ValueError("Координаты блока вне допустимого диапазона")

def save_world():
    save_level_data('level.dat.gz')
    print("Мир сохранен в level.dat.gz")

def load_world():
    if os.path.exists('level.dat.gz'):
        load_level_data('level.dat.gz')
        print("Мир загружен из level.dat.gz")
    else:
        print("Файл level.dat.gz не найден, создаем новый мир.")
        initialize_level()

def send_level_to_client(client):
    # Отправляем пакет инициализации уровня
    level_init_packet = create_level_initialize_packet()
    with client.lock:
        client.socket.sendall(level_init_packet)
    print("Пакет инициализации уровня отправлен клиенту.")
    
    # Получаем сжатые данные уровня и разбиваем на чанки
    compressed_level_data = get_compressed_level_data()
    total_chunks = (len(compressed_level_data) + 1023) // 1024
    
    for i in range(total_chunks):
        chunk_data = compressed_level_data[i*1024:(i+1)*1024]
        percent_complete = int((i + 1) / total_chunks * 100)
        level_data_chunk_packet = create_level_data_chunk_packet(chunk_data, percent_complete)
        with client.lock:
            client.socket.sendall(level_data_chunk_packet)
        print(f"Пакет данных уровня {i+1}/{total_chunks} отправлен клиенту.")
    
    # Отправляем пакет завершения уровня
    X_SIZE, Y_SIZE, Z_SIZE = get_level_dimensions()
    level_finalize_packet = create_level_finalize_packet(X_SIZE, Y_SIZE, Z_SIZE)
    with client.lock:
        client.socket.sendall(level_finalize_packet)
    print("Пакет завершения уровня отправлен клиенту.")
