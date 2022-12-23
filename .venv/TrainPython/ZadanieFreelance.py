print('Создать одномерный массив из 12 элементов. Найти в нем колво цифр 7')

import random
import re

find_figure = 7
mas = []
for i in range(12):
    mas.append(random.randint(5, 10))
# print(mas)
count = 0
for i in mas:
    if i == find_figure:
        count += 1
print(f'Количество {find_figure} в списке {mas} равно: ', count)


print('\nСоздать два списка. В одном города Украины, в другом соотв-е кол-во ' \
  'населения')

import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Города_Украины_(по_численности_населения)'
response = requests.get(url, timeout=10)
assert response.status_code == 200, 'BAD RESPONCE'
# print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
info = soup.select('.wikitable tr td')
# print(len(info))
cities, peoples, regions = [], [], []

for i in range(0, len(info), 4):
    city = 'г.' + info[i].select('a')[0].text.strip()
    citizen = info[i+2].text.replace(' ', '').strip()
    region = info[i+1].text.strip() + 'обл.'
    cities.append(city)
    peoples.append(int(citizen))
    regions.append(region)
new_dict = dict(zip(cities, peoples))

print(new_dict)

for k,v in new_dict.items():
    if v >= 1000000:
        print(k, v)


print('\nЗадание: Создать массив игроков и количество забитым мячей')
import faker

fake = faker.Faker('ru')

name, goals = [], []
for i in range(7):
    name.append(fake.last_name())
    goals.append(random.randint(0, 10))
info_games = dict(zip(name, goals))
# print(info_games)
for k, v in info_games.items():
    if v == max(goals):
        print(f'Максимальное количество мячей {v} забил игрок {k}')


print('\nЗадание: Дан массив. Найти сумму, среднее, макс, мин')

ent_list = [12, 10, 23, 27, 39, 50]

maxim = max(ent_list)
minim = min(ent_list)
summa = sum(ent_list)

print('Сумма чисел массива: ', summa)
print('Минимальное число массива: ', minim)
print('Максимальное число массива: ', maxim)
print('Среднее массива: ', round(summa/len(ent_list), 2))


print('\nЗадание: Найти численность по областям')
import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Список_регионов_Украины_по_численности_населения'

response = requests.get(url, timeout=10)
assert response.status_code == 200, 'BAD RESPONCE'
# print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
info = soup.select('.wikitable tbody tr')
# print(len(info))
regs, naselen = [], []
for i in range(2, len(info)):
    region = info[i].select('a')[1].text.strip('▼ \n')
    naselenie = info[i].select('td')[4].text.replace(' ', '').strip('▼ ▲\n')
    nas = re.match(r'\d+', str(naselenie)).group(0)
    for_up_down = info[i].select('td')[4].text.replace(' ', '').strip('\n')
    up_down = re.match(r'[^\d]', str(for_up_down)).group(0)
    if region == '[5]':
        region = 'АР Крым'
    if region == 'Севастополь':
        break
    regs.append((region, up_down))
    naselen.append(int(nas))
    # print(region, nas, up_down)
maxim_nas = max(naselen)
minim_nas = min(naselen)

new_dict = dict(zip(regs, naselen))
with open('Files/people_ukr.txt', 'w', encoding='utf-8') as file:
    file.write(str(new_dict))

for k, v in new_dict.items():
    if v == maxim_nas:
        print('Максимум: ', k[0], v, 'количество людей: ', k[1])
    if v == minim_nas:
        print('Минимум: ', k[0], v, 'количество людей: ', k[1])

print('\nЗадание. Пузырьковая сортировка по возрастанию')

a = [3, 56, 78, 94, 2, 0, 89, 23, 34, 43]
if a == False:
    for i in range(10):
        a.append(int(input(f'Enter {i+1} element of list: ')))
print('Your list: ', a)

for i in range(len(a)):
    minim = a[i]
    m = i
    j = i + 1
    while j < len(a):
        if a[j] < minim:
            minim = a[j]
            m = j
        j = j + 1
    a[m] = a[i]
    a[i] = minim
print('Your sorted list: ', a)

for i in range(len(a)):
    for i in range(len(a)-1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
print('Bubles sorted method: ', a)


print('\nЗадание: ')
# Відомі відстані до Сонця таких планет сонячної системи (у мільйонах кілометрів): земля –
# 150, Юпітер – 780, Меркурій – 58, Марс – 228, Сатурн – 1400, Венера – 108. Визначити
# назви планет, якнайдалі та якнайближче від Сонця.

# Другой вариант нахождения численности населения по областям и городам

# mas1 = ['Земля', 'Юпитер', 'Меркурий', 'Марс', 'Сатурн', 'Венера']
# mas2 = [150, 780, 58, 228, 1400, 108]
mas1 = ['Киев', 'Харьков', 'Одесса', 'Днепр', 'Запорожье', 'Львов', 'Кривой '
                                    'Рог', 'Винница', 'Херсон', 'Полтава']
mas2 = [2868702, 1451132, 1017022, 1001094, 766268, 729038, 652137,
               372116, 297593, 295950]

n = len(mas1)
mindist = mas2[0]
maxdist = mas2[0]
j, k = 0, 0

for i in range(n):
    if mas2[i] < mindist:
        mindist = mas2[i]
        j = i
    if mas2[i] > maxdist:
        maxdist = mas2[i]
        k = i
# print(f'Минимальное расстояние до Солнца {mas2[j]} км. у планеты {mas1[j]}')
# print(f'Максимальное расстояние до Солнца {mas2[k]} км. у планеты {mas1[k]}')
print(f'Минимальная численность населения {mas2[j]} человек в городе {mas1[j]}')
print(f'Максимальная численность населения {mas2[k]} человек в городе'
      f' {mas1[k]}')

index = 0
for i in range(len(mas2)):
    if mas2[i] >= 1000000:
        index = i
        print(f'В городе {mas1[index]} численность населения {mas2[index]}')



