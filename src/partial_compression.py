import zlib
import gzip

def try_partial_zlib_decompression(data, offset, length=1024):
    try:
        # Attempt to decompress a portion of the data starting at the given offset
        decompressed_data = zlib.decompress(data[offset:offset + length])
        print(f"Partial zlib decompression successful at offset {offset:08X} (first 100 bytes): {decompressed_data[:100]}")
        return decompressed_data
    except zlib.error as e:
        print(f"Partial zlib decompression failed at offset {offset:08X}: {e}")
        return None

def try_partial_gzip_decompression(data, offset, length=1024):
    try:
        # Attempt to decompress a portion of the data starting at the given offset
        decompressed_data = gzip.decompress(data[offset:offset + length])
        print(f"Partial GZIP decompression successful at offset {offset:08X} (first 100 bytes): {decompressed_data[:100]}")
        return decompressed_data
    except gzip.BadGzipFile as e:
        print(f"Partial GZIP decompression failed at offset {offset:08X}: {e}")
        return None

def read_and_attempt_partial_decompression(file_path):
    # Step 1: Read the entire file into memory
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Step 2: Offsets identified for zlib and GZIP markers
    zlib_offsets = [0x3334A, 0x2E59C]
    gzip_offsets = [0xECF32]
    
    # Step 3: Try partial decompression for each zlib offset
    for i, offset in enumerate(zlib_offsets, start=1):
        print(f"\nAttempting partial zlib decompression at offset {offset:08X}")
        try_partial_zlib_decompression(data, offset)
    
    # Step 4: Try partial decompression for each GZIP offset
    for i, offset in enumerate(gzip_offsets, start=1):
        print(f"\nAttempting partial GZIP decompression at offset {offset:08X}")
        try_partial_gzip_decompression(data, offset)

# Replace with the path to your binary file
read_and_attempt_partial_decompression('data/DB_1116.gdb')
