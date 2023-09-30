import collections
from prettytable import PrettyTable
import math
import os


def calculate_statistics(path: str) -> None:
    # Чтение файла и подсчет символов
    with open(path, 'rb') as file:
        content = file.read()
        n = len(content)
        frequencies = collections.Counter(content)

    print(f"Длина файла в символах: {n}\n")
    frequencies = dict(sorted(frequencies.items()))
    # Рассчет вероятностей и количества информации
    probabilities = {char: freq / n for char, freq in frequencies.items()}
    information_content = {char: (-math.log2(prob)) for char, prob in probabilities.items()}
    table = PrettyTable()
    table.field_names = ["Символ", "Частота", "Вероятность", "Количество Информации"]
    for key in frequencies:
        table.add_row([f"Hex: {hex(key)[2:]} ", frequencies[key], probabilities[key], information_content[key]])
        # table.add_row([f"Hex: {hex(key)[2:]} -> Dec: {key} -> Char: {chr(key)}", frequencies[key], probabilities[key],
        #               information_content[key]])
    print("Сортировка по алфавиту:")
    print(table)
    table = table.get_string(sortby="Частота")
    print("Сортировка по частотам:")
    print(table)
    # Суммарное количество информации
    total_information = n * sum([information_content[key] * probabilities[key] for key in information_content])
    print(f"\nСуммарное количество информации в битах: {total_information:.4f}")
    print(f"Суммарное количество информации в байтах: {total_information / 8:.4f}")

    return None


if __name__ == "__main__":
    file_path = "example.txt"  # Замените путь к вашему файлу
    calculate_statistics(file_path)
