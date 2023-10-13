import sys
def compress_RLE(data):
    compressed_data = bytearray()

    i = 0
    while i < len(data):
        count = 1
        while i + count < len(data) and data[i + count] == data[i]:
            count += 1

        if count > 3:
            compressed_data.append(1)  # Флаг сжатой цепочки
            compressed_data.extend((count - 3).to_bytes(1, 'big'))  # Количество повторений - 3
            compressed_data.append(data[i])  # Символ
        else:
            compressed_data.append(0)  # Флаг несжатой цепочки
            compressed_data.extend((count - 1).to_bytes(1, 'big'))  # Количество различных символов - 1
            compressed_data.extend(data[i:i + count])  # Сами символы

        i += count

    return compressed_data


def decompress_RLE(compressed_data):
    decompressed_data = bytearray()

    i = 0
    while i < len(compressed_data):
        flag = compressed_data[i]

        if flag == 1:  # Сжатая цепочка
            count = int.from_bytes(compressed_data[i + 1:i + 2], 'big') + 3
            char = compressed_data[i + 2]
            decompressed_data.extend([char] * count)
            i += 3
        else:  # Несжатая цепочка
            count = int.from_bytes(compressed_data[i + 1:i + 2], 'big') + 1
            decompressed_data.extend(compressed_data[i + 2:i + 2 + count])
            i += 2 + count

    return decompressed_data


if __name__ == "__main__":
    # Пример использования
    original_data = b'AAAABBBCCCDD'
    print(f"Before RLE: {sys.getsizeof(original_data)}")
    compressed_data = compress_RLE(original_data)
    print(f"After RLE: {sys.getsizeof(compressed_data)}")
    decompressed_data = decompress_RLE(compressed_data)

    print("Исходные данные:", original_data)
    print("Сжатые данные:", compressed_data)
    print("Распакованные данные:", decompressed_data)
    print(type(decompressed_data))
