letters_dict = {
    'q': 'й',
    'w': 'ц',
    'e': 'у',
    'r': 'к',
    't': 'е',
    'y': 'н',
    'u': 'г',
    'i': 'ш',
    'o': 'щ',
    'p': 'з',
    '[': 'х',
    ']': 'ї',
    'a': 'а',
    's': 'і',
    'd': 'в',
    'f': 'а',
    'g': 'п',
    'h': 'р',
    'j': 'о',
    'k': 'л',
    'l': 'д',
    ';': 'ж',
    "'": 'є',
    'z': 'я',
    'x': 'ч',
    'c': 'с',
    'v': 'м',
    'b': 'и',
    'n': 'т',
    'm': 'ь',
    ',': 'б',
    '.': 'ю',
    '/': '.',
    'Q': 'Й',
    'W': 'Ц',
    'E': 'У',
    'R': 'К',
    'T': 'Е',
    'Y': 'Н',
    'U': 'Г',
    'I': 'Ш',
    'O': 'Щ',
    'P': 'З',
    '[': 'Х',
    ']': 'Ї',
    'A': 'Ф',
    'S': 'І',
    'D': 'В',
    'F': 'А',
    'G': 'П',
    'H': 'Р',
    'J': 'О',
    'K': 'Л',
    'L': 'Д',
    ':': 'Ж',
    '"': 'Є',
    'Z': 'Я',
    'X': 'Ч',
    'C': 'С',
    'V': 'М',
    'B': 'И',
    'N': 'Т',
    'M': 'Ь',
    '<': 'Б',
    '>': 'Ю',
    '?': ',',
    '@': '"',
    '#': '№',
    '$': ';',
    '^': ':',
    '&': '?'
}


def replace_characters(string, char_dict):
    new_string = ""
    for char in string:
        if char in char_dict:
            new_string += char_dict[char]
        else:
            new_string += char
    return new_string


input_string = input("Enter string: ")
new_string = replace_characters(input_string, letters_dict)
print(new_string)
