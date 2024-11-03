import struct

def read_binary(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Parse the first 4 bytes as ASCII text
    header = data[0:4].decode('ascii')
    print("Header:", header)
    
    # Example: Read 4 bytes from offset 0x08 as unsigned int
    some_int = struct.unpack_from('<I', data, 0x08)[0]
    print("Integer at 0x08:", some_int)
    
    # Example: Read 4 bytes from offset 0x10 as float
    some_float = struct.unpack_from('<f', data, 0x10)[0]
    print("Float at 0x10:", some_float)
    
    # Example: Read 8 bytes from offset 0x120 as double
    some_double = struct.unpack_from('<d', data, 0x120)[0]
    print("Double at 0x120:", some_double)
    
    # Example: Read 4 bytes from offset 0x130 as UNIX timestamp
    timestamp = struct.unpack_from('<I', data, 0x130)[0]
    import datetime
    date_time = datetime.datetime.utcfromtimestamp(timestamp)
    print("Date-Time at 0x130:", date_time)

# Path to your binary file
read_binary('data/DB_1116.gdb')
