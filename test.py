from mfs import *


def generateClaude(input_text):
    output_text = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": input_text
            }
        ]
    )
    return clean_text(output_text)


print(generate_simple_ai("greetings, good sir"))
