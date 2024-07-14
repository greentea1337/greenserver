from datatypes import read_byte, read_string

def handle_player_identification(data):
    if len(data) < 131:
        raise ValueError("Недостаточно данных для пакета идентификации игрока")

    offset = 0
    packet_id, offset = read_byte(data, offset)
    protocol_version, offset = read_byte(data, offset)
    username, offset = read_string(data, offset, 64)
    verification_key, offset = read_string(data, offset, 64)
    unused, offset = read_byte(data, offset)

    return {
        "packet_id": packet_id,
        "protocol_version": protocol_version,
        "username": username,
        "verification_key": verification_key,
        "unused": unused
    }