# import time
#

# import re
# from encodings import euc_kr
# # -*- coding: cp949 -*-
# # as per recommendation from @freylis, compile once only
# CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
#
#
# def cleanhtml(raw_html) -> str:
#     cleantext = re.sub(CLEANR, '', raw_html.decode('cp949'))
#     cleantext = cleantext.replace('\n', '')
#     return cleantext
#
#
# text = '''
# '''.encode('euc_kr')
# s = '탇'
# print(s.encode('euc_kr'))
# print(s.encode('euc_kr').decode('cp949'))
# text.decode('cp949')
# print(cleanhtml(text).encode('euc_kr').decode('cp949'))
# pass
# my_list = []
#
#
# def print_list(list_local):
#     for item in list_local:
#         if str(type(item)) == "<class 'int'>":
#             my_list.append(item)
#         elif str(type(item)) == "<class 'list'>":
#             print_list(item)
#
#
# print_list([1, [2], 3, [3, [4, 5]]])
# print(my_list)
# "az".upper()
# my_list = sorted('zac')
# print(''.join([str(elem) for elem in my_list]))

# from collections import defaultdict
#
# my_list = ['key1', 'key1', 'key1']
#
#
# def get_anagrams(source):
#     d = defaultdict(list)
#     for word in source:
#         key = "".join(sorted(word))
#         d[key].append(word)
#     return d
#
#
# def print_anagrams(word_source):
#     d = get_anagrams(word_source)
#     for key, anagrams in d.items():
#         if len(anagrams) > 1:
#             print(len(anagrams))
#
#
# word_source = my_list
# print_anagrams(word_source)


# fib = lambda n: n if n <= 1 else fib(n - 1) + fib(n - 2)
#
# print([fib(n) for n in range(1, 10)])

# firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument('--proxy-server=%s' % proxies)
# driver = webdriver.Firefox(executable_path=r'C:\Users\inter\source\Python\Projects\deepl-web\geckodriver.exe')
# resp = driver.get(url)
# print(resp)
# driver.close()
