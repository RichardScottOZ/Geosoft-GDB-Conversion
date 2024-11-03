import zlib
import gzip

def decompress_zlib(data, offset, output_file):
    try:
        # Attempt decompression from the given offset
        decompressed_data = zlib.decompress(data[offset:])
        print(f"Successfully decompressed zlib data at offset {offset:08X}. Saving to {output_file}")
        
        # Save the decompressed data to a file for analysis
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
            
        return decompressed_data
    except zlib.error as e:
        print(f"Failed to decompress zlib data at offset {offset:08X}: {e}")
        return None

def decompress_gzip(data, offset, output_file):
    try:
        # Wrap the GZIP data in a file-like object for decompression
        decompressed_data = gzip.decompress(data[offset:])
        print(f"Successfully decompressed GZIP data at offset {offset:08X}. Saving to {output_file}")
        
        # Save the decompressed data to a file for analysis
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
            
        return decompressed_data
    except gzip.BadGzipFile as e:
        print(f"Failed to decompress GZIP data at offset {offset:08X}: {e}")
        return None

def read_and_decompress(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Offsets identified for zlib and GZIP markers
    zlib_offsets = [0x3334A, 0x2E59C]
    gzip_offsets = [0xECF32]
    
    # Process zlib sections
    for i, offset in enumerate(zlib_offsets, start=1):
        output_file = f'decompressed_zlib_{i}.bin'
        print(f"\nAttempting to decompress zlib data at offset {offset:08X}")
        decompress_zlib(data, offset, output_file)
    
    # Process GZIP sections
    for i, offset in enumerate(gzip_offsets, start=1):
        output_file = f'decompressed_gzip_{i}.bin'
        print(f"\nAttempting to decompress GZIP data at offset {offset:08X}")
        decompress_gzip(data, offset, output_file)

# Replace with the path to your binary file
read_and_decompress('data/DB_1116.gdb')
