# 이 코드는 텍스트 데이터에서 단어 벡터를 학습하여 단어 간 의미 관계를 파악하는데 사용되며, 이러한 워드 임베딩 모델을 활용하여 다양한 자연어 처리 작업을 수행할 수 있습니다.
import os

from gensim.models import Word2Vec

with open('data/refined_div_europe_review_list.txt', 'rt', encoding='utf-8') as f:
    div_review_list = f.read().splitlines()

tokens = []
for div_review in div_review_list:
    token = div_review.split()
    tokens.append(token)

if not os.path.isdir('models/'):
    os.mkdir('models/')

embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=5, workers=12, epochs=100, sg=1)
embedding_model.save('./models/word2vec_review.model')
# print(list(embedding_model.wv.index_to_key))
