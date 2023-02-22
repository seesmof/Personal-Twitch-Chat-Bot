def translate(text):
    translation_table = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е',
        'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
        '[': 'х', ']': 'ї', 'a': 'ф', 's': 'і', 'd': 'в',
        'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
        'l': 'д', ';': 'ж', "'": 'є', 'z': 'я', 'x': 'ч',
        'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
        ',': 'б', '.': 'ю',
    }
    # Convert the message
    translated_text = ''
    for char in text:
        if char.lower() in translation_table:
            if char.islower():
                translated_text += translation_table[char.lower()]
            else:
                translated_text += translation_table[char.lower()].upper()
        else:
            translated_text += char
    return translated_text

def main():
    text = input("Enter: ")
    print(translate(text))

if __name__ == '__main__':
    main()