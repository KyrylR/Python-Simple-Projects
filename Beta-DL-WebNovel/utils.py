import json
from os import path
from time import time


def performance(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'It took {t2 - t1} s')
        return result

    return wrapper


def writeJasonToFile(filename: str, data) -> None:
    with open(filename, 'w+') as file:
        json.dump(data, file)


def readFromJsonFile(filename: str):
    data = None
    if not fileExist(filename):
        return None, False
    with open(filename, 'r') as file:
        data = json.load(file)
    return data, True


def fileExist(filename: str) -> bool:
    return path.exists(filename)


def prettifyStr(string):
    string = string.replace('\n', '').strip()
    res = ""
    for item in string.split():
        if item == '':
            continue
        res += item + " "
    return res


def findFirstNumber(string: str):
    for i, c in enumerate(string):
        if c.isdigit():
            start = i
            while i < len(string) and string[i].isdigit():
                i += 1
            return int(string[start:i])
    return None


if __name__ == "__main__":
    pass
