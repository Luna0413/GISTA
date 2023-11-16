from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import requests
import json



#이미지 다운로드 함수
def download_image(url, local_filename):
    response = requests.get(url, stream=True)
    with open("data/"+local_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


# 크롬드라이버 경로 설정 방법 
# 1. 자신의 크롬의 버전을 확인한다. ex) 119.0.6045.124
# 2. 자신의 크롬 버전과 앞자리가 같은 크롬 드라이버 버전을 다운로드 한다 ex) 119.0.50XX.XX
# 3. 압축 해제후 크롬 드라이버 버전의 경로룰 아래의 executable_path에 입력한다. 


# 크롬드라이브 경로 설정
driver = webdriver.Chrome(executable_path="C:/your/chromedriver/path/chromedriver.exe")

#------------------------------로그인----------------------------------------
driver.get("https://www.instagram.com/accounts/login/")

try:
    main_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'input'))
    )
except Exception as e:
    print(f"Error: {e}")
    driver.quit()


# username, password 자신의 아이디 비밀번호로 사용
u_input = driver.find_element_by_name('username')
u_input.send_keys('user_id')
p_input = driver.find_element_by_name('password')
p_input.send_keys('user_password')

login_btn = driver.find_element_by_css_selector('button[type="submit"]')
login_btn.click()
time.sleep(5)

#------------------------------해시태그 입력------------------------------------
# 검색할 해시태그 입력
tag = input('검색할 해시태그를 입력하세요 : ')


driver.get("https://www.instagram.com/explore/tags/"+ tag + "/")

#print(html)

try:
    main_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'main'))
    )
except Exception as e:
    print(f"Error: {e}")
    driver.quit()


html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

"""
html 파일 
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
"""

# 이미지 태그의 클래스를 추출
img_elements = soup.find_all('img', {'alt': True, 'src': True}) 
target_links = soup.find_all('a', class_=["x1a2a7pz", "_a6hd"])
output = {} # (src : hashtag) 딕셔너리

# 추출된 이미지 태그의 클래스
for i, image in enumerate(img_elements[2:]):
    hashtags = []
    src_value = image['src']
    alt_value = image['alt']
    hashtags.extend(re.findall(r'#\w+', alt_value))
    print("-------------------------------------------")
 
    local_filename = tag + str(i+1) + ".jpg"
    download_image(src_value, local_filename)
    output[local_filename] = hashtags 
    print(local_filename)
    print(hashtags)
    print("")
    
k = 1
for a in target_links:
    href = a['href']
    if href and href.startswith('/p/'):
        local_filename = tag + str(k) + ".jpg"
        driver.get("https://www.instagram.com"+ href)
        try:
            button_element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x87ps6o.x1d5wrs8[role="button"]'))
            )
            button_element.click()
            print("Button Clicked!")
            time.sleep(0.5)
            try:
                elements_with_aa9_class = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a._aa9_'))
                )

                comment_hashtag = []
                for element in elements_with_aa9_class:
                    text_content = element.text
                    
                    if text_content.startswith('#'):
                        comment_hashtag.append(text_content)
                        print(text_content)

                output[local_filename] = comment_hashtag
  

            except Exception as e:
                print(f"Error: {e}")


        except Exception as e:
            print(f"Error: {e}")

        print(local_filename)
        print(output[local_filename])
        k += 1



    
with open('data/'+tag+'.json', 'w') as json_file:
    json.dump(output, json_file)
print(len(output.keys()))
#driver.quit()
