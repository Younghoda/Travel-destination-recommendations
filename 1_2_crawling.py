import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

#  읽기 모드('rt')
if not os.path.isfile('./paths/chrome_driver_path.txt'):
    with open('install_Chrome_driver.py', 'rt', encoding='utf-8') as file:
        exec(file.read())

with open('./paths/chrome_driver_path.txt', 'rt') as file:
    service = Service(file.read())

options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari'
              '/537.36')
options.add_argument('user_agent=' + user_agent)

driver = webdriver.Chrome(service=service, options=options)

try:
    with open('./url_list/url_list_final', 'rt') as f:
        landmark_urls = f.read().splitlines()
except FileNotFoundError:
    with open('3-2_remove_duplicate_landmarks.py', 'rt') as f:
        exec(f.read())

# os.path.isdir 함수를 사용하여 현재 디렉토리에 crawling_data 디렉토리가 존재하지 않는지 확인합니다.
# 디렉토리가 없으면, 새로운 crawling_data 디렉토리를 생성합니다.
if not os.path.isdir('./crawling_data/'):
    os.mkdir('./crawling_data/')

REFRESH_INTERVAL = 10
REVIEW_CNT_MAX = 150
URL_START_IDX = 243

countries = []
cities = []
landmarks = []
review_concats = []

for landmark_url in landmark_urls[URL_START_IDX:]:
    driver.get(landmark_url)

    # ActionChains 객체를 생성하고, 이 객체를 사용하여 다양한 동작을 연결할 수 있는 작업 영역을 만듭니다. driver는 Selenium 웹 드라이버 객체를 나타냅니다.
    actions = ActionChains(driver)
    # send_keys 메서드를 사용하여 키보드 입력을 시뮬레이션합니다. 여기서 Keys.PAGE_DOWN은 Page Down 키를 나타내며, 이를 사용하여 아래로 스크롤하는 동작을 수행합니다.
    actions.send_keys(Keys.PAGE_DOWN).perform()

    # country, city, landmark 가져옵니다.
    a_elements = driver.find_elements(By.CLASS_NAME, 'gl-component-bread-crumb_item')
    country = a_elements[3].text
    city = a_elements[-2].text
    landmark = a_elements[-1].text


    review_concat = ''
    review_cnt = 0
    prev_p_element = None
    # time.perf_counter() - start_cnt > REFRESH_INTERVAL: REFRESH_INTERVAL 시간이 경과하면, 페이지에서 다음 리뷰 페이지로 이동하기 위해 "다음" 버튼을 클릭합니다.
    # 이렿게 하면 새로운 리뷰가 로드됩니다.
    start_cnt = time.perf_counter()
    while review_cnt < REVIEW_CNT_MAX:  # infinite loop for crawling reviews of a landmark
        # review paragraph elements(리뷰 요소)
        p_elements = driver.find_elements(By.CSS_SELECTOR, 'p[class*=\'hover-pointer \']')
        # 중복 검사: 이전에 크롤링한 리뷰와 새로 크롤링한 리뷰를 비교하여 중복된 리뷰가 없으면 다음 단계로 진행합니다.
        if not p_elements or p_elements[0] == prev_p_element:
            print(1)
            if time.perf_counter() - start_cnt > REFRESH_INTERVAL:  # at least 10s
                # press the next button
                div_element = driver.find_element(By.CSS_SELECTOR, 'div[class=\'gl-cpt-pagination \']')
                try:
                    btn_element = div_element.find_element(By.CSS_SELECTOR, 'button[class=\'btn-next \'')
                except NoSuchElementException:
                    break
                while True:  # infinite loop for button click
                    try:
                        btn_element.click()
                    except ElementClickInterceptedException:
                        continue
                    break

                start_cnt = time.perf_counter()
            continue

        # 리뷰 개수가 최대값을 넘지 않도록 하기 위해
        if review_cnt + len(p_elements) > REVIEW_CNT_MAX:
            p_elements = p_elements[:REVIEW_CNT_MAX - review_cnt]

        cur_review_cnt = len(p_elements)

        temp_concat = ''
        try:
            # 전처리
            for p_element in p_elements:
                temp_concat = temp_concat + ' ' + re.compile('[^가-힣]').sub(' ', p_element.text)
        except StaleElementReferenceException:
            continue
        # 리뷰 연속으로 저장
        review_concat = review_concat + temp_concat
        # 리뷰 개수 저장
        review_cnt += cur_review_cnt

        prev_p_element = p_elements[0]

        div_element = driver.find_element(By.CSS_SELECTOR, 'div[class=\'gl-cpt-pagination \']')
        try:
            btn_element = div_element.find_element(By.CSS_SELECTOR, 'button[class=\'btn-next \'')
        except NoSuchElementException:
            break
        while True:  # infinite loop for button click
            try:
                btn_element.click()
            except ElementClickInterceptedException:
                print(3)
                continue
            break

        start_cnt = time.perf_counter()

    countries.append(country)
    cities.append(city)
    landmarks.append(landmark)
    review_concats.append(review_concat)

    # temporal save
    with open('./crawling_data/country_europe_list.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % country)
    with open('./crawling_data/city_europe_list.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % city)
    with open('./crawling_data/landmark_europe_list.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % landmark)
    with open('./crawling_data/review_europe_list.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % review_concat)




