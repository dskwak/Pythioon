import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_and_append_data(url, json_filename='output.json'):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")

    # 특정 클래스의 li 요소 선택
    tags = soup.select('li.css-8atqhb.mantine-1avyp1d')

    # 텍스트와 img src, a href 추출하여 저장
    results = []
    for tag in tags:
        item = {}
        name_tag = tag.select_one('.mantine-Text-root.css-1r49xhh.mantine-17j39m6')
        explain_tag = tag.select_one('.mantine-Text-root.css-10bh5qj.mantine-169r75g')
        img_tag = tag.find('img')
        link_tag = tag.find('a', href=True)

        if name_tag:
            item['name'] = name_tag.get_text(strip=True)
        if explain_tag:
            item['explain'] = explain_tag.get_text(strip=True)
        if img_tag:
            item['image'] = img_tag['src']
        else:
            item['image'] = 'No image'
        if link_tag:
            item['link'] = link_tag['href']
        else:
            item['link'] = 'No link'
        
        results.append(item)
    
    # 기존 데이터를 로드하거나 새로운 리스트 생성
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # 새로운 데이터를 기존 데이터에 추가
    existing_data.extend(results)

    # JSON 파일로 저장
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"Data from {url} has been appended to {json_filename}")

# 페이지 번호에 따라 URL 생성
base_url = 'https://www.inflearn.com/courses?charge=FREE&isDiscounted=false&page_number='
urls = [base_url + str(page_number) for page_number in range(1, 24)]

# 각 URL에 대해 데이터 가져오기 및 저장
for url in urls:
    fetch_and_append_data(url)
