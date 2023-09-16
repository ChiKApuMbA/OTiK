import os
# def file_to_hex(filename):
#     with open(filename, "rb") as file:
#         data = file.read()
#     hex_representation = data.hex()
#     hex_representation = [hex_representation[i:i + 2] for i in range(0, len(hex_representation), 2)]
#     return hex_representation
#
#
# def print_hex(hex_representation):
#     for i in range(len(hex_representation)):
#         if (i + 1) % 16 == 0:
#             print(hex_representation[i])
#         else:
#             print(hex_representation[i], end=" ")
#     print()
#
#
# file_path = "./test.zip"
a = 4
print(a.to_bytes(4, byteorder="little"))
with open("my_arc.gleb", "rb") as f:
    f.seek(77)
    content = f.read().hex()
print(type(content))