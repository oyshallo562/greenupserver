import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

# 브라우저 띄우지 않고 하기
options = ChromeOptions()
options.add_argument('headless')

url = 'https://search.danawa.com/dsearch.php?query=%EC%82%BC%EB%8B%A4%EC%88%98&originalQuery=%EC%82%BC%EB%8B%A4%EC%88%98&checkedInfo=N&volumeType=vmvs&page=1&limit=40'

driver = Chrome()
driver.get(url)

# 없는것을 만들어야할때.
#more_btn = WebDriverWait(driver, 5).until(
#            EC.presence_of_element_located([By.CSS_SELECTOR, 'dl#dlMaker_simple button.btn_spec_view.btn_view_more'])
#            ).click()

# 제조사 체크박스 클릭
# 있는것을 찾을때 -> 대기가 필요하다면 time.sleep이용
# driver.find_element_by_css_selector('dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(12)').click()
# element는 하나만 찾고, elements는 여러개 찾음-> a[0]이런식으로 찾아야함

# 검색결과가 렌더링 될때까지 잠시 대기
time.sleep(2)

# 5page
for page in range(1,2):

    soup = BeautifulSoup(driver.page_source, features="html.parser")
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
        print(name, img_link)