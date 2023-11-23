import logging
import os
import argparse
import random
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from typing import List
from time import sleep

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

# Функция для получения страницы и возврата объекта BeautifulSoup для парсинга
def get_page(page: int, base_url: str = "https://irecommend.ru/content/fix-price-moskva") -> BeautifulSoup:
    try:
        url = f"{base_url}{page}"
        sleep_time = random.uniform(1, 3)
        sleep(sleep_time)
        headers = {"User-Agent": generate_random_user_agent()}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        logging.exception(f"Ошибка получения страницы: {e.args}")
        return None
    except Exception as e:
        logging.exception(f"Необработанная ошибка: {e.args}")
        return None

# Функция для получения списка отзывов из объекта BeautifulSoup
def get_list_of_reviews(soup: BeautifulSoup) -> List[BeautifulSoup]:
    try:
        reviews = soup.find('ul', class_="list-comments").find_all('li')
        return reviews
    except Exception as e:
        logging.exception("Ошибка получения списка отзывов:", e)

# Функция для извлечения текста из объекта отзыва BeautifulSoup
def review_text(review: BeautifulSoup) -> str:
    try:
        text_element = review.find('div', class_="reviewTextSnippet")
        if text_element is not None:
            return text_element.get_text()
        else:
            return "Текст не найден в отзыве"
    except Exception as e:
        logging.exception("Ошибка получения текста отзыва:", e)

# Функция для определения статуса отзыва на основе количества звезд
def status_review(review: BeautifulSoup) -> str:
    try:
        stars = review.find_all(class_='on')
        count = len(stars)
        if count == 1:
            return '1'
        elif count == 2:
            return '2'
        elif count == 3:
            return '3'
        elif count == 4:
            return '4'
        elif count == 5:
            return '5'
    except Exception as e:
        logging.exception("Ошибка определения статуса отзыва:", e)

# Функция для сохранения отзыва в файл в соответствующем каталоге
def save_review_to_file(review_text: str, status_review: str, review_1: int, review_2: int, review_3: int, review_4: int, review_5: int, output_dir: str):
    if status_review == "1":
        folder_name = "1"
        file_name = f"{review_1:04d}.txt"
    elif status_review == "2":
        folder_name = "2"
        file_name = f"{review_2:04d}.txt"
    elif status_review == "3":
        folder_name = "3"
        file_name = f"{review_3:04d}.txt"
    elif status_review == "4":
        folder_name = "4"
        file_name = f"{review_4:04d}.txt"
    elif status_review == "5":
        folder_name = "5"
        file_name = f"{review_5:04d}.txt"

    file_path = os.path.join(output_dir, folder_name, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(review_text)
    except Exception as e:
        logging.exception(f"Ошибка сохранения отзыва: {e}")
