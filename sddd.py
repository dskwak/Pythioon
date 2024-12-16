import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ChromeDriver 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 열지 않음
driver = webdriver.Chrome(service=service, options=options)

# 데이터 저장 리스트 및 링크 확인 집합
data_list = []
links_set = set()

# 페이지 순회
for page in range(1, 15):
    url = f"https://edu.goorm.io/category/programming?page={page}&sort=newest&is_toll=false"
    driver.get(url)
    time.sleep(3)  # 페이지가 로드될 때까지 대기

    # 페이지 소스를 가져와서 BeautifulSoup로 파싱
    sourcecode = driver.page_source
    soup = BeautifulSoup(sourcecode, "html.parser")

    # 기본 URL 설정
    base_url = "https://edu.goorm.io"

    # 필요한 데이터 추출
    div = soup.find("div", class_="_3KgXgz")
    if div:
        for a_tag in div.find_all("a", class_="sledSW"):
            href = a_tag.get("href")
            if href:
                full_url = base_url + href
                if full_url not in links_set:
                    links_set.add(full_url)
                    title_div = a_tag.find("div", class_="B2zuzM card-title")
                    title = title_div.get_text(strip=True) if title_div else "제목 없음"
                    
                    image_div = a_tag.find("div", class_="A75fbL _1Oh39x card-img-top")
                    image_url = ""
                    if image_div and 'background-image' in image_div['style']:
                        image_url = image_div['style'].split('url(')[-1].split(')')[0]
                        image_url = image_url.strip('"').strip("'")
                    
                    data = {
                        "explain": title,
                        "image": image_url,
                        "link": full_url
                    }
                    data_list.append(data)
    else:
        print(f"지정된 div를 찾을 수 없습니다. 페이지: {page}")

# 드라이버 종료
driver.quit()

# JSON 파일로 저장
with open('new.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("데이터가 new.json 파일에 저장되었습니다.")
