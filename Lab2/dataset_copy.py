import os
import logging
import shutil
import json
import create_annotation

logging.basicConfig(level=logging.INFO)


def unify_dataset(dataset: str, unified_dataset: str, classes: list) -> None:
    """Creates a copy of {dataset} folder while replacing subfolder division with {class}_{number}.txt naming format"""
    path_list = list()
    if not os.path.exists(os.path.join(unified_dataset)):
        os.mkdir(os.path.join(unified_dataset))
    cnt = 0
    for cls in classes:
        files_count = len(os.listdir(os.path.join(dataset, cls)))
        for i in range(files_count):
            normal = os.path.abspath(os.path.join(dataset, cls, f'{i:04}.txt'))
            unified = os.path.abspath(os.path.join(unified_dataset, f'{cls}_{i:04}.txt'))
            shutil.copy(normal, unified)
            path_set = [
                [unified,
                 os.path.relpath(unified),
                 cls,]
            ]
            path_list += path_set
            cnt += 1
    return path_list


if __name__ == '__main__':
    with open(os.path.join("Lab2", "settings.json"), "r") as settings:
        settings = json.load(settings)
    uni_pathlist = unify_dataset(os.path.join(settings['directory'], settings['dataset_folder']),
                                 os.path.join(settings['directory'], settings['dataset_copy']), 
                                 settings['classes'])
    create_annotation.write_into_file((os.path.join(settings['csv_folder'], settings['dataset_copy_csv'])), uni_pathlist)