# Instagram Hashtag Crawler

## 개요
이 프로그램은 Instagram에서 지정한 해시태그의 이미지를 크롤링하는 스크립트입니다. Selenium과 BeautifulSoup을 사용하여 Instagram에 로그인하고, 특정 해시태그로 검색하여 이미지를 수집합니다.

## requirement 설치

    pip install -r requirement.txt
    
## 사용된 라이브러리
- Selenium
- BeautifulSoup
- requests
- json

## 실행 환경 설정
1. 크롬드라이버 버전에 맞게 다운로드

    참고: 크롬드라이버는 본인의 크롬 버전에 맞게 다운로드하고 경로를 설정해야 합니다.
   
    크롬 드라이버의 가장 앞 부분만 맞으면 됩니다. ex) 크롬 버전 : 119.0.6045.124 / 드라이버 버전 : 119.0.80XX.XX
   
3. crawler.py 코드에서 크롬드라이버의 경로를 설정
    ```python
    # 크롬드라이브 경로 설정
    driver = webdriver.Chrome(executable_path="your/chromedriver/path/chromedriver.exe")
    ```

4. Instagram 로그인 정보 입력
    ```python
    # Instagram 로그인 정보 입력
    u_input = driver.find_element_by_name('username')
    u_input.send_keys('your_id')
    p_input = driver.find_element_by_name('password')
    p_input.send_keys('your_password')
    ```

## 사용법
1. python ./crawler.py 실행
2. 검색할 hashtag 입력
3. 이미지는 'data' 폴더에 다운로드되며, JSON 파일로 이미지 파일명과 해당 이미지에 대한 해시태그가 저장됩니다.

## 결과물
- 이미지 파일과 해당 이미지에 대한 해시태그는 JSON 파일로 저장됩니다. 파일명은 입력한 해시태그와 동일합니다.
    - 예: `data/your_hashtag.json`, `data/your_hashtag.jpg`




