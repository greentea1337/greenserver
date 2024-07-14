from datatypes import write_byte, write_short

def create_level_finalize_packet(x_size, y_size, z_size):
    packet_id = 0x04
    data = write_byte(packet_id)
    data += write_short(x_size)
    data += write_short(y_size)
    data += write_short(z_size)
    return data
