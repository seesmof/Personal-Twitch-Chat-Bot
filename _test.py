import g4f


def main():
    prompt = input(": ")

    response = g4f.ChatCompletion.create(
        model=g4f.Model.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )

    print(response)


while True:
    main()
