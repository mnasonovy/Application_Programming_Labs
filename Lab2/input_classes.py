import os
import json
import create_annotation
import dataset_copy
import dataset_random



if __name__ == '__main__':
    with open(os.path.join('Lab2', 'settings.json'), 'r') as settings:
        settings = json.load(settings)
    if settings['mode'] == 'main':
        create_annotation.create_annotation_file(settings['dataset_main'], settings['main_csv'])
    if settings['mode'] == 'dataset_random':
        dataset_random.random_dataset(settings['dataset_main'],settings['dataset_random'],settings['default_number'],settings['classes'])
    if settings['mode'] == 'copy_dataset':
        dataset_copy(settings['dataset_main'], settings['dataset_copy'], settings['classes'])