import pandas as pd

# CSV 파일을 DataFrame으로 읽어옵니다.
df = pd.read_csv('./url_list/url_list.csv')

# 중복 행을 제거합니다.
df = df.drop_duplicates()

# 'URL' 열에 '?locale=ko-KR&curr=KRW' 문자열이 없는 행을 삭제합니다.
df = df[df['URL'].str.contains('\?locale=ko-KR&curr=KRW')]

# 중복이 제거된 DataFrame을 다시 CSV 파일로 저장합니다.
df.to_csv('./url_list/url_list_final', index=False, header=None)


