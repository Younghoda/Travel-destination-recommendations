import os
import collections

import pandas as pd
from matplotlib import font_manager
import matplotlib.pyplot as plt
import gdown

from wordcloud import WordCloud


LANDMARK_IDX = 23  # -2 in df_all.csv

font_path = 'fonts/malgun.ttf'

if not os.path.isfile('fonts/malgun.ttf'):
    gdown.download(
        'https://drive.google.com/uc?id=1a647msm7ciE6LXh2yQWYVJLU7eQp4TTn',
        font_path, quiet=True
    )

font_name = font_manager.FontProperties(fname=font_path).get_name()
# matplotlib 라이브러리의 폰트 설정을 변경하여 한글 폰트를 'NanumBarunGothic'으로 설정합니다. 이렇게 설정하면 그래프나 차트에 한글 글꼴을 적용할 수 있게 됩니다.
plt.rc('font', family='NanumBarunGothic')

if not os.path.isfile('datasets/df_all.csv'):
    with open('4_2_concat_dfs.py', 'rt') as f:
        exec(f.read())

df = pd.read_csv('datasets/df_all.csv')

# 'LANDMARK_IDX' 위치에 있는 행(레코드)에서 3번째 열(인덱스 3)의 내용을 가져와 공백을 기준으로 단어로 분할합니다.
# 'collections.Counter'를 사용하여 단어 리스트에서 각 단어의 빈도수를 계산하고, 이를 사전 형태로 변환합니다.
# 계산된 단어 빈도수를 출력합니다.
words = df.iloc[LANDMARK_IDX, 3].split()
word_dict = collections.Counter(words)
word_dict = dict(word_dict)
print(word_dict)

# 이 코드는 'wordcloud' 라이브러리를 사용하여 단어 빈도수 정보를 기반으로 워드 클라우드를 생성하고, Matplotlib를 사용하여 시각화합니다.
# 결과적으로, 빈도수에 따라 단어가 시각적으로 표현되는 워드 클라우드 이미지가 화면에 출력됩니다.
wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
).generate_from_frequencies(word_dict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()
