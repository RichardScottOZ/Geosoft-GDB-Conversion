def extract_segment(data, offset, length=500):
    # Extract data around the offset to inspect it more closely
    start = max(0, offset - 100)  # Start 100 bytes before offset
    end = offset + length          # Go 500 bytes past offset
    segment = data[start:end]
    
    # Save to file for external inspection
    output_file = f'segment_{offset:08X}.bin'
    with open(output_file, 'wb') as f:
        f.write(segment)
    
    print(f"Saved segment around offset {offset:08X} to {output_file}")
    return segment

# Example of use
with open('data/DB_1116.gdb', 'rb') as file:
    data = file.read()
    offsets = [0x3334A, 0x2E59C, 0xECF32]
    for offset in offsets:
        extract_segment(data, offset)
