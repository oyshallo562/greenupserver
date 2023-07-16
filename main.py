from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import time
import json
import urllib.parse


app = FastAPI()

display = Display(visible=0, size=(1920, 1080))
display.start()

path='/usr/bin/chromedriver'

@app.get("/scrap")
async def scrap(query: str):
    #options = ChromeOptions()
    #options.add_argument('headless')
    service = Service(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.set_capability("pageLoadStrategy", "eager")

    query = urllib.parse.quote(query)  # URL에 삽입할 수 있도록 쿼리를 인코딩합니다.

    url = f'https://search.danawa.com/dsearch.php?query={query}&originalQuery={query}&checkedInfo=N&volumeType=vmvs&page=1&limit=40'

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
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

    return results
