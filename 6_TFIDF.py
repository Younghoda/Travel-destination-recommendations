# 이 코드는 텍스트 데이터를 TF-IDF로 변환하여 단어의 중요도를 수치화하고,
# 변환된 데이터를 저장하여 나중에 머신 러닝 모델에 사용할 수 있도록 준비하는 작업을 수행합니다.
import os

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
from scipy.io import mmwrite


if not os.path.isfile('datasets/df_all.csv'):
    with open('4-2_concat_dfs.py', 'rt') as f:
        exec(f.read())

df = pd.read_csv('datasets/df_all.csv')
df.info()

tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['review'])
print(tfidf_matrix.shape)

if not os.path.isdir('objects/'):
    os.mkdir('objects/')

dump(tfidf_vectorizer, 'objects/tfidf_vectorizer.joblib')
mmwrite('objects/matrix_landmark_morpheme.mtx', tfidf_matrix)
