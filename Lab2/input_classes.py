import os
import json
import create_annotation
import dataset_copy  
import dataset_random  

if __name__ == '__main__':
    with open(os.path.join('Lab2', 'settings.json'), 'r') as settings_file:
        settings = json.load(settings_file)
        
    mode = settings.get('mode')

    if mode == 'main':
        create_annotation.create_annotation_file(settings['dataset_main'], settings['main_csv'])
    elif mode == 'dataset_random':
        dataset_random.random_dataset(settings['dataset_main'], settings['dataset_random'], settings['default_number'], settings['classes'])
    elif mode == 'copy_dataset':
        dataset_copy.copy(settings['dataset_main'], settings['dataset_copy'] + '.json', settings['classes'])  
