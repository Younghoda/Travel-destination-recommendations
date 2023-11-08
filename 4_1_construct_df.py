import os

import pandas as pd


if not os.path.isfile('data/refined_div_europe_review_list.txt'):
    with open('3_refine_morphemes.py', 'rt') as f:
        exec(f.read())

with open('crawling_data/country_europe_list.txt', 'rt', encoding='utf-8') as f:
    countries = f.read().splitlines()
with open('crawling_data/city_europe_list.txt', 'rt', encoding='utf-8') as f:
    cities = f.read().splitlines()
with open('crawling_data/landmark_europe_list.txt', 'rt', encoding='utf-8') as f:
    landmarks = f.read().splitlines()
with open('data/refined_div_europe_review_list.txt', 'rt', encoding='utf-8') as f:
    reviews = f.read().splitlines()

df_landmark_review = pd.DataFrame({
    'country': countries,
    'city': cities,
    'landmark': landmarks,
    'review': reviews
})

# 중복제거
df_landmark_review.drop_duplicates(subset='landmark', inplace=True, keep='first')
df_landmark_review.info()

if not os.path.isdir('datasets/'):
    os.mkdir('datasets/')

df_landmark_review.to_csv('datasets/df_europe.csv', index=False)
