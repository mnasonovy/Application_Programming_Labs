import os
import json
import create_annotation
import dataset_copy
import dataset_random


if __name__ == '__main__':
    with open(os.path.join('Lab2', 'settings.json'), 'r') as settings:
        settings = json.load(settings)
    if settings['mode'] == 'path_list':
        path_list = create_annotation.make_pathlist(settings['dataset_folder'], settings['classes'])
        create_annotation.write_into_file(os.path.join(settings['csv_folder'], settings['dataset_csv']), path_list)
    if settings['mode'] == 'randomize':
        path_list = dataset_random.randomize_dataset(os.path.join(settings['directory'], settings['dataset_folder']), 
                                      os.path.join(settings['directory'], settings['dataset_random']), 
                                      settings['classes'],  
                                      settings['default_size'])
        create_annotation.write_into_file((os.path.join(settings['csv_folder'], settings['dataset_random_csv'])), path_list)
    if settings['mode'] == 'unify':
        path_list = dataset_copy.unify_dataset(os.path.join(settings['directory'], settings['dataset_folder']),
                                 os.path.join(settings['directory'], settings['dataset_copy']), 
                                 settings['classes'])
        create_annotation.write_into_file((os.path.join(settings['csv_folder'], settings['dataset_copy_csv'])), path_list)