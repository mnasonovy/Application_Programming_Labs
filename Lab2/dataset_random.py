import os
import shutil
import random
import json
import csv


def random_dataset(dataset: str, random_dataset: str, size: int, classes: list, csv_file_name: str) -> None:
    """Создает папку, где файлы из random_dataset получают случайные имена."""
    rand_list = list(range(size))
    random.shuffle(rand_list)
    random_idx = rand_list

    path_list = []
    if not os.path.exists(random_dataset):
        os.mkdir(random_dataset)

    count = 0
    for cls in classes:
        files_count = len(os.listdir(os.path.join(dataset, cls)))
        for i in range(files_count):
            source_path = os.path.abspath(os.path.join(dataset, cls, f'{i:04}.txt'))
            target_path = os.path.abspath(os.path.join(random_dataset, f'{random_idx[count]:04}.txt'))
            shutil.copy(source_path, target_path)
            path_set = [
                [
                    target_path.ljust(80),
                    os.path.basename(target_path).ljust(30),
                    cls.ljust(30)
                ]
            ]
            path_list += path_set
            count += 1

    csv_file_path = os.path.join(os.getcwd(), csv_file_name)
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            'Absolute Path'.ljust(80),
            'Relative Path'.ljust(30),
            'Class'.ljust(30)
        ])
        csv_writer.writerows(path_list)


if __name__ == '__main__':
    with open(os.path.join('Lab2', 'settings.json'), 'r') as settings_file:
        settings = json.load(settings_file)

    random_dataset(settings['dataset_main'], settings['dataset_random'], settings['default_number'],
                   settings['classes'], settings['random_csv'])
