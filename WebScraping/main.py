import pprint

import requests
from bs4 import BeautifulSoup

hn = []


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(votes_s, soup):
    for idx, item in enumerate(votes_s):
        points = int(votes_s[idx].getText().replace(' points', ''))
        if points > 99:
            id = votes_s[idx].get('id').replace("score_", "")
            tr = soup.find_all("tr", attrs={"id": id})[0]
            link = tr.contents[4].contents[0]
            title = link.getText()
            href = link.get('href', None)
            hn.append({'title': title, 'votes': points, 'href': href})
    return sort_stories_by_votes(hn)


def start_scrap(pages):
    res = []
    for page in range(1, pages + 1):
        res = requests.get(f'https://news.ycombinator.com/news?p={page}')
        soup = BeautifulSoup(res.text, 'html.parser')
        votes = soup.select('.score')
        res = create_custom_hn(votes, soup)

    return res


pprint.pprint(start_scrap(2))
