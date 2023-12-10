import os
import csv
import json


"""
    Создает аннотацию в CSV файле

    Аргументы:
    - dataset: Путь к основному каталогу набора данных
    - output_file: Путь и имя файла для сохранения аннотаций в формате CSV
"""

def create_annotation_file(dataset, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                'Absolute Path'.ljust(100),
                'Relative Path'.ljust(50),
                'Class'.ljust(30)
            ])

            for file_dataset, subfolders, files_list in os.walk(dataset):
                for file_name in files_list:
                    if file_name.endswith('.txt'):
                        absolute_path = os.path.abspath(os.path.join(file_dataset, file_name)).ljust(100)
                        relative_path = os.path.relpath(absolute_path, os.path.dirname(__file__)).ljust(50)
                        class_name = os.path.basename(file_dataset).ljust(30)
                        csv_writer.writerow([absolute_path, relative_path, class_name])
    except Exception as e:
        pass


if __name__ == "__main__":
    with open(os.path.join('Lab2', 'settings.json'), 'r') as settings:
        settings = json.load(settings)
    create_annotation_file(settings['dataset_main'], settings['main_csv'])
