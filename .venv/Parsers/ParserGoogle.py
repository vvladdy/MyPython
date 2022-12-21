from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup

TIME_OUT = 10


def worker(queue: Queue):
    while True:

        film = queue.get()

        # film = 'avatar'
        print('[WORKING ON]', film)


        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
        }

        params = {
            "q": f"{film} 4k background",
            "tbm": "isch",
            "hl": "en",
            "gl": "us",
            "ijn": "0"
        }

        html = requests.get("https://www.google.com/search", params=params,
                            headers=headers)
        # print(html.text)
        soup = BeautifulSoup(html.text, "lxml")

        all_script_tags = soup.select("script")

        matched_images_data = "".join(
            re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags))
        )

        matched_images_data_fix = json.dumps(matched_images_data)
        print(matched_images_data_fix)
        matched_images_data_json = json.loads(matched_images_data_fix)
        matched_google_image_data = re.findall(
            r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}',
            matched_images_data_json)
        matched_google_images_thumbnails = ", ".join(
            re.findall(
                r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                str(matched_google_image_data))).split(", ")
        thumbnails = [
            bytes(bytes(thumbnail, "ascii").decode("unicode-escape"),
                  "ascii").decode("unicode-escape") for thumbnail in
            matched_google_images_thumbnails
        ]
        removed_matched_google_images_thumbnails = re.sub(
            r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
            "", str(matched_google_image_data))
        matched_google_full_resolution_images = re.findall(
            r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
            removed_matched_google_images_thumbnails)
        full_res_images = [
            bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode(
                "unicode-escape") for img in
            matched_google_full_resolution_images
        ]
        print(full_res_images[0])

        for index, (metadata, thumbnail, original) in enumerate(
                zip(soup.select(".isv-r.PNCib.MSM1fd.BUooTd"), thumbnails,
                    full_res_images), start=1):
            google_images = {
                "title":
                    metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                        "title"],
                "link":
                    metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                        "href"],
                "source": metadata.select_one(".fxgdke").text,
                "thumbnail": thumbnail,
                "original": original
            }
            with requests.Session() as session:
                img_response = session.get(full_res_images[0]) #google_images['original'], timeout=TIME_OUT)
                image_name = f'{film}.jpg'.replace(' ', '-')

                print(image_name)
                with open(fr'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle\{image_name}', 'wb') as file:
                    file.write(img_response.content)

            # film.background = fr'D:\MyPythonFolder\MyPython\.venv\Dif_files\
            # \ImagesGoogle{image_name}'
            # film.save()

            print('DONE!!!', google_images['original'])

        # if queue.qsize() == 0:
        #     break


def main():
    # films = Film.objects.exclude(title_en='all')


    queue = Queue()

    # for item in films:
    #     queue.put(str(item.title_en), item)
    queue.put('avatar')

    max_worker = 285
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        for _ in range(max_worker):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()

# import sys
# import requests
# from bs4 import BeautifulSoup
#
#
# query = "купить айфон olx"
# query = query.replace(' ', '+')
# URL = f"https://google.com/search?q={query}"
#
# # page2 = 10, page3 = 20, page4 = 4
# URL_3 = f'https://google.com/search?q={query}&start=20'
#
# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
#
# headers = {"user-agent" : USER_AGENT}
# resp = requests.get(URL_3, headers=headers)
# print(resp.status_code)
#
# if resp.status_code == 200:
#     soup = BeautifulSoup(resp.content, "html.parser")
#     urls = soup.select('.yuRUbf a')
#     for i in range(len(urls)):
#         href = urls[i].get('href')
#         # print(href)
#     pict = soup.select('.wXeWr')
#     print(pict)
#
#     # temp = sys.stdout
#     # sys.stdout = open(r'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\log'
#     #                   r'.txt', 'w')
#     # print(resp.content)
#     #
#     # sys.stdout.close()
#     # sys.stdout = temp
# # with open(r'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\log.txt',
# #           'r') as file:
# #     soup = BeautifulSoup(file.read(), 'html.parser')
# #
# #     urls = soup.select('.yuRUbf a')
# #     for i in range(len(urls)):
# #         href = urls[i].get('href')
# #         print(href)
#
#
# #
# # import requests
# # from bs4 import BeautifulSoup
# #
# #
# # query = "serega"
# # query = query.replace(' ', '+')
# # URL = f'https://www.google.com/search?q={query}&source=lnms&tbm=isch&sa=X'
# #
# # USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# #
# # headers = {"user-agent" : USER_AGENT}
# # resp = requests.get(URL, headers=headers)
# # print(resp.status_code)
# #
# # if resp.status_code == 200:
# #     soup = BeautifulSoup(resp.content, "html.parser")
# #     with open('picturesgoogle.txt', 'w', encoding='utf-8') as file:
# #         file.write(resp.text)
# #
# #
# # with open('picturesgoogle.txt', 'r', encoding='utf-8') as file:
# #     soup = BeautifulSoup(file.read(), "html.parser")
# #
# #     script_ser = soup.find_all('script')[75]
# #     print(script_ser)
