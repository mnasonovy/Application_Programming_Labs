import logging
import os
import argparse

# Функция для парсинга аргументов командной строки
def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to gather data from a website and save it into a dataset")
    parser.add_argument("--output_dir", type=str, default="dataset", help="Path to the directory to save the dataset")
    parser.add_argument("--base_url", type=str, default="https://irecommend.ru/content/internet-magazin-ozon-kazan-0?page=", help="Base URL for data collection")
    parser.add_argument("--pages", type=int, default=60, help="Number of pages to scrape")
    return parser.parse_args()

logging.basicConfig(level=logging.INFO)
