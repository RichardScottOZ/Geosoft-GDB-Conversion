import zlib
import gzip

def decompress_zlib(data, offset):
    try:
        # Attempt decompression starting from the given offset
        decompressed_data = zlib.decompress(data[offset:])
        print(f"Decompressed zlib data from offset {offset:08X} (first 100 bytes): {decompressed_data[:100]}")
        return decompressed_data
    except zlib.error as e:
        print(f"Failed to decompress zlib data at offset {offset:08X}: {e}")
        return None

def decompress_gzip(data, offset):
    try:
        # Gzip requires wrapping the data in a file-like object
        decompressed_data = gzip.decompress(data[offset:])
        print(f"Decompressed GZIP data from offset {offset:08X} (first 100 bytes): {decompressed_data[:100]}")
        return decompressed_data
    except gzip.BadGzipFile as e:
        print(f"Failed to decompress GZIP data at offset {offset:08X}: {e}")
        return None

def read_and_decompress(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Found offsets for zlib and GZIP markers
    zlib_offsets = [0x3334A, 0x2E59C]
    gzip_offsets = [0xECF32]
    
    # Process zlib sections
    for offset in zlib_offsets:
        print(f"\nAttempting to decompress zlib data at offset {offset:08X}")
        decompressed_data = decompress_zlib(data, offset)
    
    # Process GZIP sections
    for offset in gzip_offsets:
        print(f"\nAttempting to decompress GZIP data at offset {offset:08X}")
        decompressed_data = decompress_gzip(data, offset)

# Replace with the path to your binary file
read_and_decompress('data/DB_1116.gdb')
