from datatypes import write_byte

def create_level_initialize_packet():
    packet_id = 0x02
    data = write_byte(packet_id)
    return data
