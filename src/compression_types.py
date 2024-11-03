def search_for_patterns(file_path):
    # Known compression signatures and their descriptions
    patterns = {
        b'\x78\x9C': 'zlib (deflate)',
        b'\x78\xDA': 'zlib (deflate)',
        b'\x1F\x8B': 'GZIP',
        b'\x42\x5A\x68': 'BZIP2',
        b'\xFD\x37\x7A\x58\x5A\x00': 'LZMA',
        b'\x50\x4B\x03\x04': 'ZIP'
    }

    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Search for each pattern in the binary data
    for pattern, description in patterns.items():
        offset = data.find(pattern)
        if offset != -1:
            print(f"Found {description} compression marker at offset {offset:08X}")
        else:
            print(f"{description} marker not found")

# Replace with the path to your binary file
search_for_patterns('data/DB_1116.gdb')
