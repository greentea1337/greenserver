from datatypes import write_byte, write_short, read_byte, read_short

def create_set_block_packet(x, y, z, block_type):
    packet_id = 0x06
    data = write_byte(packet_id)
    data += write_short(x)
    data += write_short(y)
    data += write_short(z)
    data += write_byte(block_type)
    return data

def handle_set_block_packet(data):
    offset = 0
    packet_id, offset = read_byte(data, offset)
    x, offset = read_short(data, offset)
    y, offset = read_short(data, offset)
    z, offset = read_short(data, offset)
    block_type, offset = read_byte(data, offset)
    
    if packet_id != 0x06:
        raise ValueError("Invalid packet ID for Set Block packet.")
    
    return {
        'x': x,
        'y': y,
        'z': z,
        'block_type': block_type
    }
