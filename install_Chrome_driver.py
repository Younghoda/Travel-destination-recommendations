# 이 코드는 Chrome 웹 브라우저를 사용하기 위한 Chrome 드라이버의 경로를 가져와서 텍스트 파일로 저장하는 역할을 합니다.
# 이렇게 저장된 경로는 이후에 Chrome 드라이버를 설정할 때 사용됩니다.
import os

from webdriver_manager.chrome import ChromeDriverManager


chrome_driver_path = ChromeDriverManager().install()

if not os.path.isdir('./paths/'):
    os.mkdir('./paths/')

with open('./paths/chrome_driver_path.txt', 'wt') as file:
    file.write(chrome_driver_path)
