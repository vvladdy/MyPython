text = 'Hello world!'

def reverse_str(text):
    chars = list(text)

    for i in range(len(chars) // 2):
        temp = chars[i]
        chars[i] = chars[len(text) - i - 1]
        chars[len(text) - i - 1] = temp

        print(chars[i])

    return ''.join(chars)

print('string', text)
print('reverse string', reverse_str(text))