import logging
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from df_works import rating_filter, lemmatize_text

logging.basicConfig(level=logging.INFO)


def build_histogram(df: pd.DataFrame, rating: int) -> None:
    """This function takes dataframe and shows its graph by class"""
    try:
        filtered_df = lemmatize_text(rating_filter(df, rating))
        reviews = ' '.join(filtered_df['Review text']).split()

        word_counts = Counter(reviews)
        top_words = dict(word_counts.most_common(10))  # Выберите топ 10 самых частых слов

        names = list(top_words.keys())
        frequencies = list(top_words.values())

        plt.bar(names, frequencies)
        plt.xlabel('Word')
        plt.xticks(rotation=90)
        plt.ylabel('Word count')
        plt.title('Word use frequency by rating')
        plt.rcParams['font.sans-serif'] = 'Arial'
        plt.rcParams['font.family'] = 'sans-serif'
        plt.show(block=True)
    except Exception as exc:
        logging.error(f"Can not build histogram: {exc}\n{exc.args}\n")
