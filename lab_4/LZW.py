def compress_LZW(data):
    dictionary = {bytes([i]): i for i in range(256)}
    result = bytearray()
    current_sequence = bytearray()

    for byte in data:
        current_sequence.append(byte)
        if bytes(current_sequence) not in dictionary:
            result.extend(dictionary[bytes(current_sequence[:-1])].to_bytes(2, 'big'))
            dictionary[bytes(current_sequence)] = len(dictionary)
            current_sequence = bytearray([byte])

    if bytes(current_sequence) in dictionary:
        result.extend(dictionary[bytes(current_sequence)].to_bytes(2, 'big'))

    return result


def decompress_LZW(compressed_data):
    dictionary = {i: bytes([i]) for i in range(256)}
    result = bytearray()
    current_code = int.from_bytes(compressed_data[:2], 'big')
    output = dictionary[current_code]
    result.extend(output)
    next_code = 256

    i = 2
    while i < len(compressed_data):
        code = int.from_bytes(compressed_data[i:i + 2], 'big')
        i += 2

        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = output + output[:1]
        else:
            raise ValueError("Bad compressed code")

        result.extend(entry)
        dictionary[next_code] = output + entry[:1]
        next_code += 1
        output = entry

    return result


if __name__ == "__main__":
    # Пример использования
    original_data = b'ABAABABAABABABA'
    compressed_data = compress_LZW(original_data)
    print(type(compressed_data))
    decompressed_data = decompress_LZW(compressed_data)

    print("Исходные данные:", original_data)
    print("Сжатые данные:", compressed_data)
    print("Распакованные данные:", decompressed_data)
    print(type(decompressed_data))
