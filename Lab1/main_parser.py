import logging
import os
import argparse
import random
from fake_useragent import UserAgent

# Функция для парсинга аргументов командной строки
def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to gather data from a website and save it into a dataset")
    parser.add_argument("--output_dir", type=str, default="dataset", help="Path to the directory to save the dataset")
    parser.add_argument("--base_url", type=str, default="https://irecommend.ru/content/internet-magazin-ozon-kazan-0?page=", help="Base URL for data collection")
    parser.add_argument("--pages", type=int, default=60, help="Number of pages to scrape")
    return parser.parse_args()

logging.basicConfig(level=logging.INFO)

# Функция для генерации случайного user-agent
def generate_random_user_agent() -> str:
    ua = UserAgent()
    return ua.random

# Функция для создания каталогов, если они не существуют
def create_directories():
    try:
        for folder_name in ["1", "2", "3", "4", "5"]:
            folder_path = os.path.join("dataset", folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
    except Exception as e:
        logging.exception(f"Error creating folder: {e.args}")

create_directories()