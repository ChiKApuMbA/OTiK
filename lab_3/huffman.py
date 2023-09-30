from collections import Counter


class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return "%s_%s" % (self.left, self.right)


def huffman_code_tree(node, left=True, binString: str = ''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + "0"))
    d.update(huffman_code_tree(r, False, binString + "1"))
    return d


def encode_huffman(content_to_encode, huffman_table):
    content = content_to_encode
    encoded_content = ""
    for char in content:
        if char in huffman_table:
            print(f"Encoded content: {huffman_table[char]}({chr(char)})")
            encoded_content += huffman_table[char]
        else:
            print(f"Символ '{char}' не найден в таблице Хаффмана.")
    padding = 8 - (len(encoded_content) % 8)
    encoded_content += "0" * padding
    print(padding)
    print(encoded_content)
    byte_array = bytearray()
    for i in range(0, len(encoded_content), 8):
        byte = encoded_content[i:i + 8]
        byte_array.append(int(byte, 2))
        # print(f"{byte_array} the len is: {len(byte_array)}")
    for byte in byte_array:
        binary_representation = bin(byte)[2:]
        print(binary_representation)
    return byte_array, padding


def decode_huffman(content, huffman_table, padding):
    byte_array = content
    # print("For decode:")
    encoded_content = ""
    for byte in byte_array:
        # print(f"Encoded content: {byte} -> {format(byte, '08b')}")
        encoded_content += format(byte, '08b')
    print(encoded_content)
    encoded_content = encoded_content[:-padding]
    print(encoded_content)
    print(len(encoded_content))
    reversed_huffman_table = {value: key for key, value in huffman_table.items()}
    decoded_content = []
    current_code = ""
    for bit in encoded_content:
        current_code += bit
        if current_code in reversed_huffman_table:
            print(f"The Decoded Content: {current_code}({reversed_huffman_table[current_code]})")
            decoded_content.append(reversed_huffman_table[current_code])
            current_code = ""
    print(decoded_content)
    byte_array = bytearray(decoded_content)
    print(byte_array)
    return byte_array


def create_huffman_codes(freak_array):
    freak_array = dict(sorted(freak_array.items(), key=lambda item: (-item[1], item[0])))
    print(freak_array)
    freq = {str(key): value for key, value in freak_array.items()}
    nodes = list(freq.items())
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    huffmancode = huffman_code_tree(nodes[0][0])
    huffmancode = {int(key): value for key, value in huffmancode.items()}
    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in huffmancode.items():
        print(f"{char:^3}({chr(char)})|{huffmancode[char]:^12}")
    return huffmancode


if __name__ == "__main__":
    with open("test.txt", "rb") as f:
        data = f.read()
    print(data)
    string = 'BCAADDDCCACACAC'
    freq = Counter(data)
    codes = create_huffman_codes(freq)
    # print(' %-4s |%12s' % (str(char), huffmanCode[char]))
    encoded_data, padding = encode_huffman(data, codes)
    decoded_data = decode_huffman(encoded_data, codes, padding)
    with open("check.txt", "wb") as f:
        f.write(decoded_data)
