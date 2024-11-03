import zlib

def try_decompress(data):
    try:
        # Attempt to decompress assuming zlib compression
        decompressed_data = zlib.decompress(data)
        print("Decompression successful!")
        return decompressed_data
    except zlib.error as e:
        print("Failed to decompress with zlib:", e)
        return None

def read_binary_with_decompression(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Assuming header is 4 bytes, and data starts after
    header = data[:4].decode('ascii')
    print("Header:", header)

    if header == "!CBD":
        # Try decompressing the remaining data after the header
        compressed_data = data[4:]
        decompressed_data = try_decompress(compressed_data)

        if decompressed_data:
            print("Decompressed data (first 100 bytes):", decompressed_data[:100])

# Replace with your actual file path
read_binary_with_decompression('data/DB_1116.gdb')
