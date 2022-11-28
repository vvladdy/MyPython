def full_name(firs: str, last: str):
    return firs.title() + ' ' + last.title()

def squares(l):
    l2 = []
    for num in range(l):
        l2.append(num**2)
    return l2

def is_even(number):
    ''' Returns True if **number** is even or False if it is odd. '''

    return True if number % 2 == 0 else False