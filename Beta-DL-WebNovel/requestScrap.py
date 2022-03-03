from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup

from utils import prettifyStr, findFirstNumber


def scrapDefault(url) -> (list, str):
    chapter_text = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.find_all('p')
    next_to_scrap = find_nextChapter_url(soup.find_all('a'), url)
    for item in temp:
        # print("0" + str(item.parent.nextSibling) + "0")
        if len(item.attrs) == 0:
            if len(item.text) < 2:
                continue
            text_to_upload = prettifyStr(item.text)
            chapter_text.append(text_to_upload)

    return chapter_text, next_to_scrap


def find_nextChapter_url(link_list: list, cur_url: str) -> str:
    try:
        result = "None"
        cur_chap_num = findFirstNumber(cur_url)
        for item in link_list:
            possible_url = item.attrs['href']
            # print(f"Ratio of {possible_url} is {SequenceMatcher(None, possible_url, cur_url).ratio()})")
            if SequenceMatcher(None, possible_url, cur_url).ratio() >= 0.95:
                next_chap_num = findFirstNumber(possible_url)
                if next_chap_num > cur_chap_num:
                    result = possible_url
                    break
        return result
    except Exception as e:
        print(e)
        return "None"


if __name__ == "__main__":
    pass
