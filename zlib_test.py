
import zlib

def compress_data(data):
    """
    Compress data using zlib.

    Args:
        data (bytes): The data to be compressed.

    Returns:
        bytes: The compressed data.
    """
    return zlib.compress(data)

def decompress_data(compressed_data):
    """
    Decompress data using zlib.

    Args:
        compressed_data (bytes): The compressed data.

    Returns:
        bytes: The decompressed data.
    """
    return zlib.decompress(compressed_data)



def uncompress_part_of_file(file_path, start_byte, end_byte):
    """
    Uncompress a part of a file using zlib.

    Args:
        file_path (str): Path to the file.
        start_byte (int): Starting byte of the part to uncompress.
        end_byte (int): Ending byte of the part to uncompress.

    Returns:
        bytes: The uncompressed part of the file.
    """
    with open(file_path, 'rb') as f:
        compressed_data = f.read(end_byte - start_byte + 1)
    return zlib.decompress(compressed_data)



def check_decompressed_data(file_path, start_byte, end_byte):
    """
    Check if the decompressed data is valid.

    Args:
        file_path (str): Path to the file.
        start_byte (int): Starting byte of the part to uncompress.
        end_byte (int): Ending byte of the part to uncompress.

    Returns:
        bool: True if the decompressed data is valid, False otherwise.
    """
    with open(file_path, 'rb') as f:
        compressed_data = f.read(end_byte - start_byte + 1)
        decompressed_data = zlib.decompress(compressed_data)
        crc32 = zlib.crc32(decompressed_data)
        return crc32 == int.from_bytes(compressed_data[4:8], byteorder='big')

