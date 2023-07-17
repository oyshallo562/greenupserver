from fastapi import FastAPI
from bs4 import BeautifulSoup
import httpx
import urllib.parse
from functools import lru_cache

app = FastAPI()

@lru_cache(maxsize=100)
async def get_data(query: str):
    async with httpx.AsyncClient() as client:
        query = urllib.parse.quote(query)
        url = f'https://search.danawa.com/dsearch.php?query={query}&originalQuery={query}&checkedInfo=N&volumeType=vmvs&page=1&limit=40'
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    product_li_tags = soup.select('li.prod_item')

    results = []

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
        img_link = "https:" + img_link

        results.append({
            "name": name,
            "img_link": img_link
        })

    return results

@app.get("/scrap")
async def scrap(query: str):
    return await get_data(query)
