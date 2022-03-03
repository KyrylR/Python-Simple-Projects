from requestScrap import scrapDefault
from workWithDocx import writeToDocx

if __name__ == "__main__":
    url = "https://moonlightnovels.com/for-your-failed-unrequited-love/ful-chapter-02/"
    counter, next_chapter = 2, ""
    while next_chapter != "None":
        (text, next_chapter) = scrapDefault(url)
        writeToDocx(text, counter)
        url = next_chapter
        counter += 1
