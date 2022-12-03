def gsd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b
a = 30
b = 18
print(f'HOД чисел {a} и {b}:', gsd(a, b))