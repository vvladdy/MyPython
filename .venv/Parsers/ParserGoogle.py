import sys
import requests
from bs4 import BeautifulSoup


query = "купить айфон olx"
query = query.replace(' ', '+')
URL = f"https://google.com/search?q={query}"

# page2 = 10, page3 = 20, page4 = 4
URL_3 = f'https://google.com/search?q={query}&start=20'

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

headers = {"user-agent" : USER_AGENT}
resp = requests.get(URL_3, headers=headers)
print(resp.status_code)

if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
    urls = soup.select('.yuRUbf a')
    for i in range(len(urls)):
        href = urls[i].get('href')
        # print(href)
    pict = soup.select('.wXeWr')
    print(pict)

    # temp = sys.stdout
    # sys.stdout = open(r'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\log'
    #                   r'.txt', 'w')
    # print(resp.content)
    #
    # sys.stdout.close()
    # sys.stdout = temp
# with open(r'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\log.txt',
#           'r') as file:
#     soup = BeautifulSoup(file.read(), 'html.parser')
#
#     urls = soup.select('.yuRUbf a')
#     for i in range(len(urls)):
#         href = urls[i].get('href')
#         print(href)


#
# import requests
# from bs4 import BeautifulSoup
#
#
# query = "serega"
# query = query.replace(' ', '+')
# URL = f'https://www.google.com/search?q={query}&source=lnms&tbm=isch&sa=X'
#
# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
#
# headers = {"user-agent" : USER_AGENT}
# resp = requests.get(URL, headers=headers)
# print(resp.status_code)
#
# if resp.status_code == 200:
#     soup = BeautifulSoup(resp.content, "html.parser")
#     with open('picturesgoogle.txt', 'w', encoding='utf-8') as file:
#         file.write(resp.text)
#
#
# with open('picturesgoogle.txt', 'r', encoding='utf-8') as file:
#     soup = BeautifulSoup(file.read(), "html.parser")
#
#     script_ser = soup.find_all('script')[75]
#     print(script_ser)
