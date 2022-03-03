import asyncio
import urllib.parse
from time import sleep

from bs4 import BeautifulSoup
from pyppeteer import launch

from utils import performance
from workWithDocx import writeToDocx, getTextFromDocx

# Global data
translate_result = []


def make_translated_data(chapter_list):
    text = ""
    res_list = []
    for count, item in enumerate(chapter_list.split("   ")):
        if item == '':
            continue
        text = text + item + '\n'
        if len(text) + len(item) + 1 > 1000:
            if count != len(chapter_list) - 1:
                res_list.append(text)
                text = item

    return res_list


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
def process(titles_list: list):
    for item in titles_list:
        global translate_result
        translate_result = []
        text = getTextFromDocx(f'data_to_translate/{item}.docx')
        asyncio.get_event_loop().run_until_complete(translate(make_translated_data(text)))
        writeToDocx(translate_result, item)


if __name__ == "__main__":
    pass
