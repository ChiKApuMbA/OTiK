def file_to_hex(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    hex_representation = data.hex()
    hex_representation = [hex_representation[i:i + 2] for i in range(0, len(hex_representation), 2)]
    return hex_representation


def split_byte_chunk(chunk):
    split_chunk = [chunk.hex()[i:i + 2] for i in range(0, len(chunk.hex()), 2)]
    return " ".join(split_chunk)


def get_color_grid(chunk):
    # t = 0
    # grid = ""
    # for i in range(len(chunk)):
    #     if (i + 1) % 8 == 0:
    #         # print(f"{0 + t} -> {i}")
    #         # print(split_byte_chunk(chunk[t:i+1]),"\n")
    #         grid += split_byte_chunk(chunk[t:i + 1]) + "\n"
    #         t += 8
    # return grid

    grid = [chunk[i:i + 16] for i in range(0, 64, 16)]
    for row in grid:
        print(split_byte_chunk(row))


def print_hex(hex_representation):
    for i in range(len(hex_representation)):
        if (i + 1) % 16 == 0:
            print(hex_representation[i])
        else:
            print(hex_representation[i], end=' ')
    print()


def read_bmp(path):
    with open(path, 'rb') as bmp_file:
        # Считываем заголовок файла (14 байт)
        file_header = bmp_file.read(14)

        # Разбираем байты заголовка файла
        file_type = file_header[:2].decode('utf-8')
        file_size = int.from_bytes(file_header[2:6], byteorder='little')
        reserved1 = int.from_bytes(file_header[6:8], byteorder='little')
        reserved2 = int.from_bytes(file_header[8:10], byteorder='little')
        pixel_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        # Считываем информационный заголовок (40 байт)
        info_header = bmp_file.read(4)

        # Разбираем байты информационного заголовка
        size_of_header = int.from_bytes(info_header, byteorder='little')
        bmp_file.seek(14)
        info_header = bmp_file.read(size_of_header)
        width = int.from_bytes(info_header[4:8], byteorder='little')
        height = int.from_bytes(info_header[8:12], byteorder='little')
        planes = int.from_bytes(info_header[12:14], byteorder='little')
        bit_count = int.from_bytes(info_header[14:16], byteorder='little')
        compression = int.from_bytes(info_header[16:20], byteorder='little')
        size_image = int.from_bytes(info_header[20:24], byteorder='little')
        x_pixels_per_meter = int.from_bytes(info_header[24:28], byteorder='little')
        y_pixels_per_meter = int.from_bytes(info_header[28:32], byteorder='little')
        colors_used = int.from_bytes(info_header[32:36], byteorder='little')
        colors_important = int.from_bytes(info_header[36:40], byteorder='little')
        # palette = int.from_bytes(info_header[40:], byteorder='little')

        # Выводим информацию о заголовке файла и информационном заголовке
        print("Заголовок файла (BitMapFileHeader):")
        print(f"Тип файла: {file_type} ({split_byte_chunk(file_header[:2])})")
        print(f"Размер файла: {file_size}({split_byte_chunk(file_header[2:6])}) байт")
        print(f"Зарезервировано 1: {reserved1}({split_byte_chunk(file_header[6:8])})")
        print(f"Зарезервировано 2: {reserved2}({split_byte_chunk(file_header[8:10])})")
        print(f"Смещение данных пикселей: {pixel_data_offset}({(split_byte_chunk(file_header[10:14]))})байт")
        print(f"\nИнформационный заголовок файла (BITMAPINFOHEADER):")
        print(f"Размер заголовка: {size_of_header} ({split_byte_chunk(info_header[:4])})")
        print(f"Ширина изображения: {width}({split_byte_chunk(info_header[4:8])}) пикселей")
        print(f"Высота изображения: {height}({split_byte_chunk(info_header[8:12])}) пикселей")
        print(f"Число цветовых плоскостей: {planes}({split_byte_chunk(info_header[12:14])})")
        print(f"Глубина цвета: {bit_count} ({split_byte_chunk(info_header[14:16])})бит/пиксель")
        print(f"Метод сжатия: {compression}({split_byte_chunk(info_header[16:20])})")
        print(f"Размер изображения в байтах: {size_image}({split_byte_chunk(info_header[20:24])}) байт")
        print(f"Горизонтальное разрешение: {x_pixels_per_meter}({split_byte_chunk(info_header[24:28])}) пикселей/метр")
        print(f"Вертикальное разрешение: {y_pixels_per_meter}({split_byte_chunk(info_header[28:32])}) пикселей/метр")
        print(f"Число используемых цветов: {colors_used}({split_byte_chunk(info_header[32:36])})")
        print(f"Число важных цветов: {colors_important}({split_byte_chunk(info_header[36:40])})")
        # print(f"Палитра: {palette}({split_byte_chunk(info_header[40:])})")
        if size_of_header == 108:
            red_channels_bit_mask = info_header[40:44]
            green_channels_bit_mask = info_header[44:48]
            blue_channel_bit_mask = info_header[48:52]
            alpha_channel_bit_mask = info_header[52:56]
            lcs_windows_color_space = info_header[56:60]
            ciexyztriple_color_space_endpoints = info_header[60:96]
            red_gamma = info_header[96:100]
            green_gamma = info_header[100:104]
            blue_gamma = info_header[104:108]
            print(f"RED CHANNELS BIT MASK: {split_byte_chunk(red_channels_bit_mask)}")
            print(f"GREEN CHANNELS BIT MASK: {split_byte_chunk(green_channels_bit_mask)}")
            print(f"BLUE CHANNELS BIT MASK: {split_byte_chunk(blue_channel_bit_mask)}")
            print(f"ALPHA CHANNELS BIT MASK: {split_byte_chunk(alpha_channel_bit_mask)}")
            print(f"LCS_WINDOWS_COLOR_SPACE: {split_byte_chunk(lcs_windows_color_space)}")
            print(f"CIEXYZTRIPLE Color Space endpoints: {split_byte_chunk(ciexyztriple_color_space_endpoints)}")
            print(f"0 RED GAMMA: {split_byte_chunk(red_gamma)}")
            print(f"0 GREEN GAMMA: {split_byte_chunk(green_gamma)}")
            print(f"0 BLUE GAMMA: {split_byte_chunk(blue_gamma)}")
            pallette = bmp_file.read(pixel_data_offset - (14 + size_of_header))
            print(f"Pallette: {split_byte_chunk(pallette)}")
        bmp_file.seek(130)
        pixel_data = bmp_file.read()
        print("Pixel array:")
        get_color_grid(pixel_data)
        # print(get_color_grid(pixel_data))
        return None


file_path = 'colorchess16x16x2.bmp'
with open(file_path, "rb") as bmp_file:
    content = bmp_file.read()

print(f"Размер файла в байтах: {len(content)}")
hex_content = file_to_hex(file_path)
print_hex(hex_content)
read_bmp(file_path)
