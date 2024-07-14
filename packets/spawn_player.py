import struct

def create_spawn_player_packet(player_id, player_name, x, y, z, yaw, pitch):
    packet_id = 0x07  # Идентификатор пакета "Spawn Player"
    player_id = (player_id & 0xFF).to_bytes(1, byteorder='big', signed=True)
    player_name = player_name.ljust(64, ' ')[:64].encode('ascii')
    x = int(x * 32).to_bytes(2, byteorder='big', signed=True)
    y = int(y * 32).to_bytes(2, byteorder='big', signed=True)
    z = int(z * 32).to_bytes(2, byteorder='big', signed=True)
    yaw = (yaw & 0xFF).to_bytes(1, byteorder='big')
    pitch = (pitch & 0xFF).to_bytes(1, byteorder='big')
    
    return packet_id.to_bytes(1, byteorder='big') + player_id + player_name + x + y + z + yaw + pitch
