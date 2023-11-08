from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

# 유럽 명소 중 리뷰가 100개 이상인 것만 나오는 url
url = 'https://kr.trip.com/travel-guide/attraction/europe-120002/tourist-attractions/comment-count-1011-100'
driver.get(url)

url_list=[]

while(1):
    # driver.find_elements(By.CLASS_NAME, 'online-poi-item-card')를 사용하여 웹 페이지에서 "online-poi-item-card" 클래스를 가진 모든 요소를 찾습니다.
    # 이 요소들은 각각의 여행 정보를 나타냅니다.
    a_elements = driver.find_elements(By.CLASS_NAME, 'online-poi-item-card')
    # 찾은 요소들을 반복하여 각 요소의 href 속성을 추출하고, 이 링크를 url_list 리스트에 추가합니다.
    for a_element in a_elements:
        url_list.append(a_element.get_attribute('href'))
    time.sleep(1)
    try:
        try:
            # class_button을 찾아옵니다. 이 버튼은 페이지를 다음으로 이동하기 위한 버튼입니다.
            class_button = driver.find_elements(By.CLASS_NAME, 'ant-pagination-item-link')[1]
        except IndexError:
            break
            # 속성에 disabled가 있으면 더이상 다음페이지로 갈 수 없기 때문에 break롤 사용했습니다.
        if class_button.get_attribute('disabled'):
            break
        while(1):
            try:
                class_button.click()
                break
            except:
                continue
    except:
        break

df_data = pd.DataFrame({'URL':url_list})
df_data.to_csv('./url_list/url_list.csv', index=False)







