import os
from pathlib import Path
import huffman


class DecoderEncoderV2:
    signature = b"\x47\x4c\x45\x42"
    file_format_ver = b"\x02"
    code_of_used_alg = b"\x00\x01"

    def decode_dir(self, arc_name: Path, dir_path: Path, amount_of_entries: int, pointer: int) -> int:
        os.mkdir(dir_path)
        print(f"The dir to decode: {dir_path}")

        print(f"Amount of entries: {amount_of_entries}")
        for i in range(amount_of_entries):
            with open(arc_name, "rb") as arc:
                print(f"Cur entry:{i}")
                print(f"Cur pointer:{pointer}")
                arc.seek(pointer)
                type_of_entry = int.from_bytes(arc.read(1), byteorder="little")
                pointer += 1
                len_of_entry_name = int.from_bytes(arc.read(2), byteorder="little")
                pointer += 2
                entry_name = arc.read(len_of_entry_name).decode(encoding="utf-8")
                pointer += len_of_entry_name
                if type_of_entry == 0:
                    file_size = int.from_bytes(arc.read(4), byteorder="little")
                    pointer += 4
                    file_content = arc.read(file_size)
                    pointer += file_size
                    print("=======================")
                    print(f"Тип entry: {type_of_entry}")
                    print(f"Длина имени entry: {len_of_entry_name}")
                    print(f"Имя entry: {entry_name}")
                    print(f"Размер entry: {file_size}")
                    print(f"Куда будет записан контент: {dir_path / entry_name}")
                    print(f"Cur pointer:{pointer}")
                    print("file")
                    print("=======================")
                    with open(dir_path / entry_name, "wb") as f:
                        f.write(file_content)
                else:
                    size_of_entries_in_dir = int.from_bytes(arc.read(4), byteorder="little")
                    pointer += 4
                    amount_of_entries_in_dir = int.from_bytes(arc.read(4), byteorder="little")
                    pointer += 4
                    print("=======================")
                    print(f"Тип entry: {type_of_entry}")
                    print(f"Длина имени entry: {len_of_entry_name}")
                    print(f"Имя entry: {entry_name}")
                    print(f"Размер entry: {size_of_entries_in_dir}")
                    print(f"Куда будет создана директория: {dir_path / entry_name}")
                    print(f"Cur pointer:{pointer}")
                    print("dir")
                    print("=======================")
                    pointer = self.decode_dir(arc_name, dir_path / entry_name, amount_of_entries_in_dir, pointer)
                    print(f"After decode_dir pointer:{pointer}")
        return pointer

    def decode(self, file_path: Path) -> None:
        with open(file_path, "rb+") as file:
            # перемещение к началу массива частот
            file.seek(11)
            amount_of_keys = int.from_bytes(file.read(2), byteorder="little")
            print(f"The amount of keys: {amount_of_keys}")
            # побайтно считываем массив частот
            freq_byte_array = file.read(amount_of_keys * 3)
            print(freq_byte_array)
            # считываем padding
            padding = int.from_bytes(file.read(1), byteorder="little")
            # считываем размер без сжатия
            # size_without_compression = int.from_bytes(file.read(4), byteorder="little")
            # print(f"Size without compression: {size_without_compression}")
            # создания словаря с частотами
            freq = {}
            for i in range(0, len(freq_byte_array), 3):
                key = freq_byte_array[i]
                value = int.from_bytes(freq_byte_array[i + 1:i + 3], byteorder="little")
                print(f"key: {key}->value: {value}")
                freq[key] = value
            # создания кодов для разжатия
            huffman_codes = huffman.create_huffman_codes(freq)
            # контент котрый нужно разжать
            content_to_decode = file.read()
            print(f"The content to decode: {content_to_decode}")
            # разжатый контент
            decoded_content = huffman.decode_huffman(content_to_decode, huffman_codes, padding)
            file.seek(7 + 1 + amount_of_keys * 3 + 1)
            file.write(decoded_content)

            file.seek(0)
            left_data = file.read(11)
            print(f"The left data:{left_data}")
            file.seek(7 + 1 + amount_of_keys * 3 + 1)
            right_data = file.read()
            print(f"The right data:{right_data}")
            file.seek(0)
            file.write(left_data + right_data)
        pointer = 0
        with open(file_path, "rb") as file:
            signature = file.read(4).decode(encoding="utf-8")
            pointer += 4
            print(signature)
            # assert signature != "GLEB", "Unknown file format"
            format_version = int.from_bytes(file.read(1), byteorder="little")
            pointer += 1
            print(format_version)
            compression_method = int.from_bytes(file.read(2), byteorder="little")
            pointer += 2
            print(f"The compression method code: {compression_method}")
            file_size_without_compression = int.from_bytes(file.read(4), byteorder="little")
            pointer += 4
            print(f"File size without compression: {file_size_without_compression}")
            amount_of_entries = int.from_bytes(file.read(4), byteorder="little")
            pointer += 4
            print(f"Amount of entries: {amount_of_entries}")
            type_of_entry = int.from_bytes(file.read(1), byteorder="little")
            pointer += 1
            len_of_entry_name = int.from_bytes(file.read(2), byteorder="little")
            pointer += 2
            entry_name = file.read(len_of_entry_name).decode(encoding="utf-8")
            pointer += len_of_entry_name
            if type_of_entry == 0:
                file_size = int.from_bytes(file.read(4), byteorder="little")
                pointer += 4
                file_content = file.read(file_size)
                pointer += file_size
                with open(entry_name, "wb") as file_entry:
                    file_entry.write(file_content)
                print(f"**********************")
                print("Считывается файл")
                print(f"Длина имени файла: {len_of_entry_name}")
                print(f"Имя файла: {entry_name}")
                print(f"Размер файла: {file_size}")
                print(f"Содержимое файла:{file_content}")
                print(f"**********************")

            else:
                size_of_entries_in_dir = int.from_bytes(file.read(4), byteorder="little")
                pointer += 4
                amount_of_entries_in_dir = int.from_bytes(file.read(4), byteorder="little")
                pointer += 4
                print(f"**********************")
                print("Считывается директория ")
                print(f"Длина имени директории: {len_of_entry_name}")
                print(f"Имя директории: {entry_name}")
                print(f"Размер директории: {size_of_entries_in_dir}")
                print(f"Количество записей директории:{amount_of_entries_in_dir}")
                print(f"Pointer:{pointer}")
                print(f"**********************")
                pointer += self.decode_dir(file_path, Path(os.getcwd(), entry_name), amount_of_entries_in_dir,
                                           pointer)
        return None

    def get_dir_size(self, directory):
        total_size = 0
        for dir_path, dir_names, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                total_size += os.path.getsize(fp)
        return total_size

    def encode_dir(self, arc_name: Path, dir_name: Path):
        with os.scandir(dir_name) as it:
            for entry in it:
                if entry.is_file():
                    with open(arc_name, "ab") as arc:
                        type_of_entry = int.to_bytes(0, byteorder="little", length=1)
                        arc.write(type_of_entry)

                        len_of_entry_name = len(entry.name).to_bytes(2, byteorder="little")
                        print(f"Длина имени файла внутри директории {dir_name}: {len_of_entry_name}")
                        arc.write(len_of_entry_name)

                        entry_name = entry.name.encode("utf-8")
                        print(f"Имя файла внутри директории {dir_name}: {entry_name}")
                        arc.write(entry_name)

                        size_of_entry = entry.stat().st_size.to_bytes(4, byteorder="little")
                        print(f"Размер файла внутри директории {dir_name}: {size_of_entry}")
                        arc.write(size_of_entry)
                        print(Path(dir_name, entry_name.decode("utf-8")))
                        with open(Path(dir_name, entry_name.decode("utf-8")), "rb") as f:
                            content = f.read()
                        arc.write(content)
                else:
                    with open(arc_name, "ab") as arc:
                        type_of_entry = int.to_bytes(1, byteorder="little", length=1)
                        arc.write(type_of_entry)

                        len_of_entry_name = len(entry.name).to_bytes(2, byteorder="little")
                        print(f"Длина имени директории внутри директории {dir_name}: {len_of_entry_name}")
                        arc.write(len_of_entry_name)

                        entry_name = entry.name.encode("utf-8")
                        print(f"Имя директории внутри директории {dir_name}: {entry_name}")
                        arc.write(entry_name)

                        size_of_entry = self.get_dir_size(dir_name / entry.name)
                        print(f"Размер директории внутри директории {dir_name}: {size_of_entry}")
                        arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))

                        amount_of_entries_in_dir = len(os.listdir(dir_name / entry_name.decode("utf-8"))).to_bytes(4,
                                                                                                                   byteorder="little")
                        print(
                            f"Количество элементов директории внутри директории {dir_name}: {amount_of_entries_in_dir}")
                        arc.write(amount_of_entries_in_dir)

                    self.encode_dir(arc_name, dir_name / entry.name)
        return None

    def encode(self, arc_name: Path, entry_path: Path) -> None:
        with open(arc_name, "ab") as arc:
            arc.write(self.signature)
            arc.write(self.file_format_ver)
            arc.write(self.code_of_used_alg)
        if os.path.isfile(entry_path):
            with open(arc_name, "ab") as arc:
                global_size_without_compression = os.path.getsize(entry_path)
                print(f"Размер файла без сжатия: {global_size_without_compression}")
                arc.write(int.to_bytes(global_size_without_compression, byteorder="little", length=4))

                global_amount_of_entries = 1
                arc.write(int.to_bytes(global_amount_of_entries, byteorder="little", length=4))

                type_of_entry = 0
                arc.write(int.to_bytes(type_of_entry, byteorder="little", length=1))

                len_of_entry_name = len(entry_path.name)
                print(f"Длина имени файла: {len_of_entry_name}")
                arc.write(int.to_bytes(len_of_entry_name, byteorder="little", length=2))

                entry_name = entry_path.name
                print(f"Имя файла: {entry_name}")
                arc.write(entry_name.encode("utf-8"))

                size_of_entry = os.path.getsize(entry_path)
                print(f"Размер файла: {size_of_entry}")
                arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))
                with open(entry_path, "rb") as f:
                    content = f.read()
                arc.write(content)

        else:
            with open(arc_name, "ab") as arc:
                global_size_without_compression = self.get_dir_size(entry_path)
                print(f"Размер центральной директории без сжатия: {global_size_without_compression}")
                arc.write(int.to_bytes(global_size_without_compression, byteorder="little", length=4))

                global_amount_of_entries = len(os.listdir(entry_path))
                print(f"Количество элементов центральной директории: {global_amount_of_entries}")
                arc.write(int.to_bytes(global_amount_of_entries, byteorder="little", length=4))

                type_of_entry = 1
                arc.write(int.to_bytes(type_of_entry, byteorder="little", length=1))

                len_of_entry_name = len(entry_path.name)
                print(f"Длина имени центральной директории: {len_of_entry_name}")
                arc.write(int.to_bytes(len_of_entry_name, byteorder="little", length=2))

                entry_name = entry_path.name
                print(f"Имя центральной директории: {entry_name}")
                arc.write(entry_name.encode("utf-8"))

                size_of_entry = self.get_dir_size(entry_path)
                print(f"Размер центральной директории: {size_of_entry}")
                arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))

                amount_of_entries_in_dir = len(os.listdir(entry_path))
                print(f"Количиство элементов центральной диретории: {amount_of_entries_in_dir}")
                arc.write(int.to_bytes(amount_of_entries_in_dir, byteorder="little", length=4))

            self.encode_dir(arc_name, entry_path)
        with open(arc_name, "rb+") as arc:
            arc.seek(11)
            content_to_compress = arc.read()
            freq = huffman.Counter(content_to_compress)
            arc.seek(11)

            arc.write(len(freq).to_bytes(2, byteorder="little"))
            tmp_freq = len(freq).to_bytes(2, byteorder="little")
            print(f"Amount of unique bytes in content: {tmp_freq}")
            for key, value in freq.items():
                arc.write(key.to_bytes(1, byteorder="little"))
                tmp_key = key.to_bytes(1, byteorder="little")

                arc.write(value.to_bytes(2, byteorder="little"))
                tmp_value = value.to_bytes(2, byteorder="little")

                print(f"key: {key}({tmp_key})->value: {value}({tmp_value})")

            huffman_codes = huffman.create_huffman_codes(freq)
            encoded_data, padding = huffman.encode_huffman(content_to_compress, huffman_codes)
            print(f"Content to compress: {content_to_compress}")
            split_chunk = [encoded_data.hex()[i:i + 2] for i in range(0, len(encoded_data.hex()), 2)]
            print(f"The encoded data is {split_chunk}")
            print(f"The padding is: {padding}")
            arc.write(padding.to_bytes(1, byteorder="little"))
            tmp_padding = padding.to_bytes(1, byteorder="little")
            print(f"The padding is: {tmp_padding}")
            arc.write(encoded_data)
            arc.truncate()
        return None


if __name__ == "__main__":
    t = DecoderEncoderV2()
    my_arc = Path(os.getcwd(), "my_arc.gleb")
    my_entry = Path(os.getcwd(), "zayavlenie2022.doc")
    # if os.path.exists(my_arc):
    #    os.remove(my_arc)

    #t.encode(my_arc, my_entry)
    t.decode(my_arc)
