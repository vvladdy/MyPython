numlist = [1, 3, 4, 4, 3, 5, 6, 7, 1, 8]

for i in range(len(numlist)):
    lowest_el = i # принимаем первый элемент за наименьший

    for j in range(i+1, len(numlist)):
        if numlist[j] < numlist[lowest_el]:
            lowest_el = j

    numlist[i], numlist[lowest_el] = numlist[lowest_el], numlist[i]
print('Sorted list: ', numlist)