from datatypes import write_byte, write_string

def create_server_identification_packet(protocol_version, server_name, server_motd, user_type):
    packet_id = 0x00
    data = write_byte(packet_id)
    data += write_byte(protocol_version)
    data += write_string(server_name, 64)
    data += write_string(server_motd, 64)
    data += write_byte(user_type)
    return data
