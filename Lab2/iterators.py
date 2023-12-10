import csv
import os
import json

"""
        Инициализирует объект FileIterator для итерации по файлам с заданными параметрами

        Аргументы:
        - file_paths: Список путей к файлам для итерации
        - classes: Список классов 
"""
class FileIterator:
    def __init__(self, file_paths: list, classes: list):
        self.file_paths = file_paths
        self.classes = classes
        self.current_index = 0

    def __iter__(self):
        return self
    
    def __next__(self) -> str:
        while self.current_index < len(self.file_paths):
            current_path = self.file_paths[self.current_index]
            self.current_index += 1
            for class_name in self.classes:
                if class_name in current_path:
                    return current_path
        raise StopIteration

if __name__ == "__main__":
    with open(os.path.join("Lab2", "settings.json"), "r") as settings_file:
        settings = json.load(settings_file)
    
    file_iterator = FileIterator(
        [os.path.join(settings["directory"], settings["random_csv"])],
        settings["classes"]
    )

    for file_path in file_iterator:
        print(file_path)
