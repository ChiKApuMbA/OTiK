import os
from pathlib import Path
from os import DirEntry


class DecoderEncoder:
    signature = b"\x47\x4c\x45\x42"
    file_format_ver = b"\x01"
    code_of_used_alg = b"\x00\x00"

    def decode_dir(self, arc_name: str, dir_name: str, amount_of_entries: int, pointer: int) -> int:
        path = os.getcwd() + f"/{dir_name}"
        os.mkdir(path)
        for i in range(amount_of_entries):
            with open(arc_name, "rb") as arc:
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
                    with open(path + f"/{entry_name}", "wb") as f:
                        f.write(file_content)
                else:
                    amount_of_entries_in_dir = int.from_bytes(arc.read(4), byteorder="little")
                    pointer += 4
                    self.decode_dir(arc_name, path + f"/{entry_name}", amount_of_entries_in_dir, pointer)
        return pointer

    def decode(self, file_path: str) -> None:
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
            for i in range(amount_of_entries):
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
                else:
                    amount_of_entries_in_dir = int.from_bytes(file.read(4), byteorder="little")
                    pointer += 4
                    pointer = self.decode_dir(file_path, entry_name, amount_of_entries_in_dir, pointer)
        return None

    def get_dir_size(self, directory):
        total_size = 0
        for dir_path, dir_names, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                print("xui")
                print(fp)
                total_size += os.path.getsize(fp)
        print(total_size)
        return total_size

    def encode_dir(self, arc_name: Path, dir_name: Path):
        with os.scandir(dir_name) as it:
            for entry in it:
                if entry.is_file():
                    with open(arc_name, "ab") as arc:
                        type_of_entry = int.to_bytes(0, byteorder="little", length=1)
                        arc.write(type_of_entry)

                        len_of_entry_name = len(entry.name).to_bytes(2, byteorder="little")
                        arc.write(len_of_entry_name)

                        entry_name = entry.name.encode("utf-8")
                        arc.write(entry_name)

                        size_of_entry = entry.stat().st_size.to_bytes(4, byteorder="little")
                        arc.write(size_of_entry)
                        print("chlen")
                        print(Path(dir_name, entry_name.decode("utf-8")))
                        with open(Path(dir_name, entry_name.decode("utf-8")), "rb") as f:
                            content = f.read()
                        arc.write(content)
                else:
                    with open(arc_name, "ab") as arc:
                        type_of_entry = int.to_bytes(1, byteorder="little", length=1)
                        arc.write(type_of_entry)

                        len_of_entry_name = len(entry.name).to_bytes(2, byteorder="little")
                        arc.write(len_of_entry_name)

                        entry_name = entry.name.encode("utf-8")
                        arc.write(entry_name)

                        size_of_entry = self.get_dir_size(entry.name)
                        arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))

                        amount_of_entries_in_dir = len(os.listdir(Path(entry_name.decode("utf-8")).resolve())).to_bytes(4, byteorder="little")
                        arc.write(amount_of_entries_in_dir)

                        self.encode_dir(arc_name, os.getcwd() + entry.name)
        return None

    def encode(self, arc_name: Path, entry_path: Path) -> None:
        with open(arc_name, "ab") as arc:
            arc.write(self.signature)
            arc.write(self.file_format_ver)
            arc.write(self.code_of_used_alg)
        if os.path.isfile(entry_path):
            with open(arc_name, "ab") as arc:
                global_size_without_compression = os.path.getsize(entry_path)
                arc.write(int.to_bytes(global_size_without_compression, byteorder="little", length=4))

                global_amount_of_entries = 1
                arc.write(int.to_bytes(global_amount_of_entries, byteorder="little", length=4))

                type_of_entry = 0
                arc.write(int.to_bytes(type_of_entry, byteorder="little", length=1))

                len_of_entry_name = len(entry_path.name)
                arc.write(int.to_bytes(len_of_entry_name, byteorder="little", length=2))

                entry_name = entry_path.name
                arc.write(entry_name.encode("utf-8"))

                size_of_entry = os.path.getsize(entry_path)
                arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))
                with open(entry_path, "rb") as f:
                    content = f.read()
                arc.write(content)

        else:
            with open(arc_name, "ab") as arc:
                global_size_without_compression = os.path.getsize(entry_path)
                arc.write(int.to_bytes(global_size_without_compression, byteorder="little", length=4))

                global_amount_of_entries = self.get_dir_size(entry_path)
                arc.write(int.to_bytes(global_amount_of_entries, byteorder="little", length=4))

                type_of_entry = 1
                arc.write(int.to_bytes(type_of_entry, byteorder="little", length=1))

                len_of_entry_name = len(entry_path.name)
                arc.write(int.to_bytes(len_of_entry_name, byteorder="little", length=2))

                entry_name = entry_path.name
                arc.write(entry_name.encode("utf-8"))

                size_of_entry = self.get_dir_size(entry_path)
                arc.write(int.to_bytes(size_of_entry, byteorder="little", length=4))

                amount_of_entries_in_dir = len(os.listdir(entry_path))
                arc.write(int.to_bytes(amount_of_entries_in_dir, byteorder="little", length=4))

            self.encode_dir(arc_name, entry_path)


# os.mkdir("/test")
# print(os.path.abspath("/test"))
t = DecoderEncoder()
# print(t.get_dir_size("some.txt"))
# t.encode("my_arc.gleb", "some.txt")

a = Path("dab.txt")
print(a.resolve(strict=False))
#my_arc = Path(os.getcwd(), "my_arc.gleb")
#my_entry = Path(os.getcwd(), "sadjgh")

#t.encode(my_arc, my_entry)
