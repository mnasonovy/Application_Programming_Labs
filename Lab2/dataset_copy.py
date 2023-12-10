import os
import logging
import shutil
import json
import csv

logging.basicConfig(level=logging.INFO)

"""
    Копирует файлы из dataset в dataset_copy с переименованием по формату {class}_{number}.txt и создает аннотацию в CSV файле
    
    Аргументы:
    - dataset: Путь к исходному каталогу с данными
    - copy_dataset: Путь к каталогу, в который будут скопированы данные
    - classes: Список классов
    - csv_file_name: Имя файла CSV, куда будут записаны абсолютные и относительные пути скопированных файлов и номер класса
    - return: None
"""
def copy_dataset(dataset: str, copy_dataset: str, classes: list, csv_file_name: str) -> None:
    path_list = []
    if not os.path.exists(copy_dataset):
        os.mkdir(copy_dataset)
    try:
        for cls_index, cls in enumerate(classes, start=1):
            files_list = os.listdir(os.path.join(dataset, cls))
            for i, file_name in enumerate(files_list, start=1):
                if file_name.endswith('.txt'):
                    source_path = os.path.abspath(os.path.join(dataset, cls, file_name))
                    target_path = os.path.abspath(os.path.join(copy_dataset, f'{cls}_{i:04}.txt'))
                    shutil.copy(source_path, target_path)
                    relative_path = os.path.relpath(target_path, os.path.abspath(os.path.join(copy_dataset, '..', '..')))
                    path_set = [
                        [
                            target_path.ljust(100),
                            relative_path.ljust(50),
                            cls.ljust(30)  # Добавляем класс в список
                        ]
                    ]
                    path_list += path_set

        csv_file_path = os.path.join(os.getcwd(), csv_file_name)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                'Absolute Path'.ljust(100),
                'Relative Path'.ljust(50),
                'Class'.ljust(30)
            ])
            csv_writer.writerows(path_list)

        logging.info(f"Файлы из {dataset} успешно скопированы в {copy_dataset}")
    except Exception as e:
        logging.error(f"Произошла ошибка в copy_dataset: {e}", exc_info=True)



if __name__ == '__main__':
    with open(os.path.join("Lab2", "settings.json"), "r") as settings_file:
        settings = json.load(settings_file)

    copy_dataset(settings['dataset_main'], settings['dataset_copy'], settings['classes'], settings['copy_csv'])
