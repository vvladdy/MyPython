import json

import openpyxl
from googletrans import Translator

# Define variable to load the dataframe
dataframe = openpyxl.load_workbook(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\1000words.xlsx')

# Define variable to read sheet
dataframe1 = dataframe.active

translator = Translator()
# filename = translator.translate(for_filename, dest='en')

info = []

# Iterate the loop to read the cell values
for row in range(0, dataframe1.max_row):
    for col in dataframe1.iter_cols(1, dataframe1.max_column):
        trans = translator.translate(col[row].value, dest='ru').text
        if len(str(col[row].value)) > 2:
            print(f'{col[row].value} - {trans}')
            info.append({
                'eng': col[row].value,
                'rus': trans
            })
with open(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\1000words.json',
          'w', encoding='utf-8') as f:
    json.dump(info, f, indent=4, ensure_ascii=False)

with open(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\1000words.json',
          'rb') as file:
    datas = json.load(file)
    filecontent = openpyxl.Workbook()

    sheet = filecontent.active

    sheet['A1'] = 'eng'.upper()
    sheet['B1'] = 'rus'.upper()

    row = 2

    for inf in datas:
        sheet[row][0].value = inf['eng']
        sheet[row][1].value = inf['rus']
        row += 1

    filecontent.save(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\1000wordtransl.xlsx')
    filecontent.close()


# Еще вариант перевода таблиц в json


# import xlwings as xw
#
# # Specifying a sheet
# ws = xw.Book("Book2.xlsx").sheets['Sheet1']
#
# # Selecting data from a single cell
# v1 = ws.range("A1:A7").value
# # v2 = ws.range("F5").value
# print("Result:", v1, v2)