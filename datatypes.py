import struct

# Функции для чтения различных типов данных из байтового массива

def read_byte(data, offset):
    """Читает один байт без знака и возвращает его значение и новый смещенный указатель."""
    value = struct.unpack_from('>B', data, offset)[0]
    return value, offset + 1

def read_sbyte(data, offset):
    """Читает один байт со знаком и возвращает его значение и новый смещенный указатель."""
    value = struct.unpack_from('>b', data, offset)[0]
    return value, offset + 1

def read_fbyte(data, offset):
    """Читает один байт со знаком, делит его значение на 32 и возвращает результат и новый смещенный указатель."""
    value = struct.unpack_from('>b', data, offset)[0] / 32.0
    return value, offset + 1

def read_short(data, offset):
    """Читает два байта (short) и возвращает его значение и новый смещенный указатель."""
    value = struct.unpack_from('>h', data, offset)[0]
    return value, offset + 2

def read_fshort(data, offset):
    """Читает два байта (short), делит его значение на 32 и возвращает результат и новый смещенный указатель."""
    value = struct.unpack_from('>h', data, offset)[0] / 32.0
    return value, offset + 2

def read_string(data, offset, length=64):
    """Читает строку заданной длины (по умолчанию 64 байта) и возвращает её значение (без завершающих пробелов) и новый смещенный указатель."""
    raw_string = struct.unpack_from(f'>{length}s', data, offset)[0]
    decoded_string = raw_string.decode('ascii').rstrip('\x20')
    return decoded_string, offset + length

def read_byte_array(data, offset, length=1024):
    """Читает массив байтов заданной длины (по умолчанию 1024 байта) и возвращает его значение и новый смещенный указатель."""
    byte_array = struct.unpack_from(f'>{length}s', data, offset)[0]
    return byte_array, offset + length

# Функции для записи различных типов данных в байтовый массив

def write_byte(value):
    """Записывает один байт без знака и возвращает его в виде байтового массива."""
    return struct.pack('>B', value)

def write_sbyte(value):
    """Записывает один байт со знаком и возвращает его в виде байтового массива."""
    return struct.pack('>b', value)

def write_fbyte(value):
    """Записывает один байт со знаком после умножения на 32 и возвращает его в виде байтового массива."""
    return struct.pack('>b', int(value * 32))

def write_short(value):
    """Записывает два байта (short) и возвращает их в виде байтового массива."""
    return struct.pack('>h', value)

def write_fshort(value):
    """Записывает два байта (short) после умножения на 32 и возвращает их в виде байтового массива."""
    return struct.pack('>h', int(value * 32))

def write_string(value, length=64):
    """Записывает строку заданной длины (по умолчанию 64 байта) и возвращает её в виде байтового массива."""
    encoded_string = value.ljust(length, '\x20').encode('ascii')
    return struct.pack(f'>{length}s', encoded_string)

def write_byte_array(value, length=1024):
    """Записывает массив байтов заданной длины (по умолчанию 1024 байта) и возвращает его в виде байтового массива."""
    return struct.pack(f'>{length}s', value)
