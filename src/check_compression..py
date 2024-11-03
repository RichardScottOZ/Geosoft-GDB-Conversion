import zlib

def is_compressed(file_path):
    with open(file_path, 'rb') as file:
        # Read the uncompressed header
        header = file.read(4)  # Assuming the header is 4 bytes long

        # Check if the header matches the expected signature
        if header == b'!CBD':
            # Read a chunk of data after the header
            chunk = file.read(1024)  # Adjust the chunk size as needed

            try:
                # Try to decompress the chunk using zlib
                decompressed_data = zlib.decompress(chunk)
                return True  # The data is compressed
            except zlib.error:
                return False  # The data is not compressed

    return False  # The file does not have the expected header

# Usage example
file_path = 'data/DB_1116.gdb'
if is_compressed(file_path):
    print("The file is compressed.")
else:
    print("The file is not compressed or does not have the expected header.")