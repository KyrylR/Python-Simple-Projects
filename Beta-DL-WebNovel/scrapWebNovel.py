import asyncio
from difflib import SequenceMatcher

from bs4 import BeautifulSoup
from pyppeteer import launch

from utils import readFromJsonFile, writeJasonToFile, fileExist, prettifyStr
from workWithDocx import writeToDocx

# Global
chapter_list_titles = []


# Only for site Web Novel
async def get_chapter_list(page, url, from_title: str, header_url: str):
    chapter_list = []
    await page.goto(url)

    temp = []
    while len(temp) < 1000:
        page_content = await page.content()
        # Process extracted content with BeautifulSoup
        soup = BeautifulSoup(page_content, features="lxml")
        print(soup.text)
        temp = soup.find_all('a')

    # next_to_scrap = soup.select('.nav-next a')[0].get('href', None)
    flag = False
    for item in temp:
        # print("0" + str(item.parent.nextSibling) + "0")
        if SequenceMatcher(None, item.text, from_title).ratio() > 0.6 or flag:
            flag = True
            chapter_list_titles.append(item.attrs['title'])
            chapter_list.append(header_url + str(item.attrs['href']))

    return chapter_list, chapter_list_titles


async def get_data_webnovel(url, from_title, header_url):
    while True:
        try:
            browser = await launch()

            # Open a new browser page
            page = await browser.newPage()

            global chapter_list_titles
            if not fileExist('listfile.txt') and not fileExist('listfile2.txt'):
                chapter_list, chapter_list_titles = await get_chapter_list(page, url, from_title, header_url)
                writeJasonToFile('listfile.txt', chapter_list)
                writeJasonToFile('listfile2.txt', chapter_list_titles)

            chapter_list, works = readFromJsonFile('listfile.txt')
            chapter_list_titles, works = readFromJsonFile('listfile2.txt')

            if not works:
                await browser.close()
                break

            await get_chapter_text(chapter_list, page, chapter_list_titles)

            # Close browser
            await browser.close()
            break

        except StopIteration as err:
            print('StopIteration Error')
            break
        except Exception as e:
            print(e)
            await browser.close()


async def get_chapter_text(chapters: list, page, titles):
    for index, item in enumerate(chapters):
        text = []
        await page.goto(item)
        page_content = await page.content()
        parse_html(text, page_content, titles, index)


def parse_html(chapter_body: list, page_content, titles, index):
    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(page_content, features="lxml")
    # print(soup.text)
    temp = soup.find_all('p')
    temp_titles = soup.find_all('h3')
    count = 0
    for index, p in enumerate(temp):
        if len(p.attrs) == 0 and p.next_element.name != 'strong':
            text_to_upload = p.text
            text_to_upload = prettifyStr(text_to_upload)
            if text_to_upload == 'Paragraph comments':
                break
            chapter_body.append(text_to_upload)
        elif p.next_element.name == 'strong':
            count += 1
            if len(chapter_body) > 10:
                print(temp_titles[count - 1].text)
                writeToDocx(chapter_body, temp_titles[count - 1].text, count - 1)
                chapter_body = []
            else:
                chapter_body = []


if __name__ == "__main__":
    # with open("data_to_translate.html", "r", encoding='utf-8') as f:
    #     text = f.read()
    # parse_html([], text, 0, 0)
    # translate.process(chapter_list_titles)
    url_catalog = "https://www.webnovel.com/book/genius-doctor-black-belly-miss_11022818606234705/catalog"
    from_title = 'Recognizing \'Father\'（2）'
    header_url = 'https://www.webnovel.com/'
    asyncio.get_event_loop().run_until_complete(get_data_webnovel(url_catalog, from_title, header_url))
