import os

from icrawler.builtin import GoogleImageCrawler

save_image_dir = r'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle'

google_crawler = GoogleImageCrawler(
    storage={'root_dir': save_image_dir}
)

name_request = 'background movies avatar'
quantity_image = 3

filters = dict(
    size='large'
)

# можно переименовать файлы
# os.rename(r'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle\00001.jpg'
#           r'', r'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle'
#                r'\avatar.jpg')

google_crawler.crawl(keyword=name_request, filters=filters,
                     max_num=quantity_image,  min_size=(400, 200))
