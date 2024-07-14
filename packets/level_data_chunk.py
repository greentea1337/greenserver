from datatypes import write_byte, write_short, write_byte_array

def create_level_data_chunk_packet(chunk_data, percent_complete):
    packet_id = 0x03
    chunk_length = len(chunk_data)
    if chunk_length < 1024:
        chunk_data = chunk_data.ljust(1024, b'\x00')
    
    data = write_byte(packet_id)
    data += write_short(chunk_length)
    data += write_byte_array(chunk_data, 1024)
    data += write_byte(percent_complete)
    return data
