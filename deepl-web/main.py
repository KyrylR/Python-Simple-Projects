import asyncio
import urllib.parse
from difflib import SequenceMatcher
from time import time, sleep

import requests
from bs4 import BeautifulSoup
from pyppeteer import launch

from Proxy import Proxy

def performance(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'It took {t2 - t1} s')
        return result

    return wrapper


def start_scrap(url):
    chapter_text = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.find_all('p')
    next_to_scrap = soup.select('.nav-next a')[0].get('href', None)
    for item in temp:
        # print("0" + str(item.parent.nextSibling) + "0")
        if SequenceMatcher(a=str(item.parent.nextSibling), b='.entry-content').ratio() > 0.6:
            if item.text == " ":
                continue
            chapter_text.append(item.text)

    return make_translated_data(chapter_text), next_to_scrap


def make_translated_data(chapter_list):
    text = ""
    res_list = []
    for count, item in enumerate(chapter_list):
        text = text + item + '\n'
        if len(text) + len(item) + 1 > 1000:
            if count != len(chapter_list) - 1:
                res_list.append(text)
                text = item

    res_list.append(text)
    return res_list


translate_result = []


async def translate(to_translate):
    # Launch the browser
    browser = await launch()

    # Open a new browser page
    page = await browser.newPage()

    for item in to_translate:
        text_raw = item
        text_raw = urllib.parse.quote(text_raw, safe='~@#$&()*!+=:;,.?/\'', encoding=None, errors=None)
        url = f'https://www.deepl.com/translator#en/ru/{text_raw}'

        # Open web page by url
        await page.goto(url)
        text = ""
        while len(text) < 10:
            sleep(0.5)
            page_content = await page.content()
            # Process extracted content with BeautifulSoup
            soup = BeautifulSoup(page_content, features="lxml")
            text = soup.find(id="target-dummydiv").get_text()

        translate_result.append(text)
    # Close browser
    await browser.close()


@performance
def process(cur_url):
    (to_trans, next_url) = start_scrap(cur_url)
    asyncio.get_event_loop().run_until_complete(translate(to_trans))
    listToStr = ' '.join([str(elem) for elem in translate_result])
    soup = BeautifulSoup(listToStr, features="lxml")
    with open("sample.html", "a+", encoding="utf-8") as file:
        file.write(soup.prettify())
    print(soup.prettify())
    return next_url


if __name__ == "__main__":
    # begin_with_site = f'https://steambunlightnovel.com/devils-son-in-law/chapter-497-long-range-raid/'
    # while True:
    #     begin_with_site = process(begin_with_site)
    proxy = Proxy()
    print(proxy := proxy.get_proxy("https://2ip.ru/"))
    res = requests.get(f"https://2ip.ru/",
                       proxies={'http': proxy})
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.text)
