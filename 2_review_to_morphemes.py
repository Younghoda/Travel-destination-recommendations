import os
import json

from konlpy.tag import Okt

# 해당 파일이 존재하지 않는다면, 이 블록 내의 코드를 실행합니다.
if not os.path.isfile('crawling_data/review_europe_list.txt'):
    with open('./1_2_crawling.py', 'rt') as f:
        exec(f.read())

# 파일을 텍스트 모드('rt')로 읽어들입니다. 이것은 review_europe_list.txt 파일의 내용을 읽어옵니다.
with open('crawling_data/review_europe_list.txt', 'rt', encoding='utf-8') as f:
    review_concats = f.read().splitlines()


okt = Okt()
div_review_list = []
for review_concat in review_concats:
    # okt.pos() 함수를 사용하여 형태소 분석을 수행합니다. stem=True 옵션은 형태소의 원형을 사용하도록 설정합니다.
    # 형태소 분석 결과는 (형태소, 품사) 형태의 튜플로 구성된 리스트입니다. 이 결과를 div_review_list에 추가합니다.
    div_review_list.append(okt.pos(review_concat, stem=True))

# 현재 디렉토리에서 data라는 디렉토리가 존재하지 않는 경우, 이 디렉토리를 생성합니다.
if not os.path.isdir('data/'):
    os.mkdir('data/')

# 형태소 분석 결과가 튜플의 리스트로 저장되어 있으므로, 이를 리스트의 리스트로 변환합니다. 각 형태소 정보를 리스트로 변환하는 작업입니다.
div_review_list = [[list(t) for t in review] for review in div_review_list]
with open('data/div_europe_review_list.json', 'wt') as f:
    # json.dump() 함수를 사용하여 div_review_list 리스트를 JSON 형식으로 파일에 저장합니다.
    json.dump(div_review_list, f)
