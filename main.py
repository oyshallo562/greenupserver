from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import urllib.parse

app = FastAPI()

@app.get("/scrap")
async def scrap(query: str):
    options = ChromeOptions()
    options.add_argument('headless')

    query = urllib.parse.quote(query)  # URL에 삽입할 수 있도록 쿼리를 인코딩합니다.

    url = f'https://search.danawa.com/dsearch.php?query={query}&originalQuery={query}&checkedInfo=N&volumeType=vmvs&page=1&limit=40'

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    results = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_li_tags = soup.select('li.prod_item')

    for li in product_li_tags:
        name_element = li.select_one('p.prod_name a')
        img_element = li.select_one('div.thumb_image a img')

        if name_element is None or img_element is None:
            continue

        name = name_element.text.strip()
        img_link = img_element.get('data-src')
        if img_link is None:
            img_link = img_element.get('src')
        img_link = img_link.replace("130:130", "300:300")

        results.append({
            "name": name,
            "img_link": img_link
        })

    driver.quit()

    return JSONResponse(content=json.dumps(results), status_code=200)
