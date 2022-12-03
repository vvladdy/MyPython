# для бинарного поиска список должен быть отсортирован

numlist = [34, 12, 4, 9, 3, 5, 6, 7, 2, 8]
sortlist = []

for i in range(len(numlist)):
    lowest = i

    for j in range(i+1, len(numlist)):
        if numlist[j] < numlist[lowest]:
            lowest = j
    numlist[i], numlist[lowest] = numlist[lowest], numlist[i]
    sortlist = numlist
print('Sort list: ', sortlist)

search_el = 2

low_el = 0
hight_el = len(numlist) - 1
index = None # индекс искомого элемента

while(low_el <= hight_el) and (index is None):
    # определяем элемент, который к середине
    mid = (low_el+hight_el) // 2

    if numlist[mid] == search_el:
        index = mid
    else:
        if search_el < numlist[mid]:
            # поиск в левой части списка
            hight_el = mid - 1
        else:
            # поиск в правой части списка
            low_el = mid + 1

print(f'Индекс элемента: {search_el} это:', index)

