import os
from pathlib import Path


class DecoderEncoder:
    signature = b"\x47\x4c\x45\x42"
    file_format_ver = b"\x01"
    code_of_used_alg = b"\x00\x00"

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
            print(compression_method)
            file_size_without_compression = int.from_bytes(file.read(4), byteorder="little")
            pointer += 4
            print(file_size_without_compression)
            amount_of_entries = int.from_bytes(file.read(4), byteorder="little")
            pointer += 4
            print(amount_of_entries)
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
                print(f"Размер файла: {entry_name}")
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
        return None


t = DecoderEncoder()
my_arc = Path(os.getcwd(), "my_arc.gleb")
my_entry = Path(os.getcwd(), "test")

#t.encode(my_arc, my_entry)
t.decode(my_arc)
