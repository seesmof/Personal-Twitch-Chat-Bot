from mfs import *

while True:
    prompt = input(": ")
    output = g4f.ChatCompletion.create(
        model=g4f.Model.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True
    )
    for message in output:
        print(message, end='')
