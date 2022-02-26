import json
from difflib import SequenceMatcher

from bs4 import BeautifulSoup
from docx import Document
from pyppeteer import launch

import translate


async def get_chapter_list(page):
    chapter_list = []
    chapter_list_titles = []
    await page.goto("https://www.webnovel.com/book/genius-doctor-black-belly-miss_11022818606234705/catalog")

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
        if SequenceMatcher(None, item.text, 'Recognizing \'Father\'（2）').ratio() > 0.6 or flag:
            flag = True
            chapter_list_titles.append(item.attrs['title'])
            chapter_list.append('https://www.webnovel.com/' + str(item.attrs['href']))

    return chapter_list, chapter_list_titles


async def get_chapter_text(chapters: list, page, titles):
    for index, item in enumerate(chapters):
        text = []
        await page.goto(item)
        page_content = await page.content()
        parse_html(text, page_content, titles, index)


def edit_str(string):
    string = string.replace('\n', '').strip()
    res = ""
    for item in string.split():
        if item == '':
            continue
        res += item + " "
    return res


def parse_html(text: list, page_content, titles, index):
    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(page_content, features="lxml")
    # print(soup.text)
    temp = soup.find_all('p')
    temp_titles = soup.find_all('h3')
    count = 0
    for index, p in enumerate(temp):
        if len(p.attrs) == 0 and p.next_element.name != 'strong':
            text_to_upload = p.text
            text_to_upload = edit_str(text_to_upload)
            if text_to_upload == 'Paragraph comments':
                break
            text.append(text_to_upload)
        elif p.next_element.name == 'strong':
            count += 1
            if len(text) > 10:
                print(temp_titles[count - 1].text)
                write_docx(text, temp_titles[count - 1].text, count - 1)
                text = []
            else:
                text = []


title_list = []


def write_docx(str_list, title, title_num):
    document = Document()

    for item in str_list:
        document.add_paragraph(item)

    document.add_page_break()

    title_name = f'#{title_num + 1}'
    title_list.append(title_name)
    document.save(f'data\{title_name}.docx')


async def get_data_webnovel():
    while True:
        try:
            browser = await launch()

            # Open a new browser page
            page = await browser.newPage()

            chapter_list, chapter_list_titles = await get_chapter_list(page)
            with open('listfile.txt', 'w+') as filehandle:
                json.dump(chapter_list, filehandle)
            with open('listfile2.txt', 'w+') as filehandle:
                json.dump(chapter_list, filehandle)

            with open('listfile.txt', 'r') as filehandle:
                chapter_list = json.load(filehandle)
            with open('listfile2.txt', 'r') as filehandle:
                chapter_list_titles = json.load(filehandle)

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


# asyncio.get_event_loop().run_until_complete(get_data_webnovel())
if __name__ == "__main__":
    with open("data.html", "r", encoding='utf-8') as f:
        text = f.read()
    parse_html([], text, 0, 0)
    translate.process(title_list)
