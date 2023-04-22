import sqlchat


def generate(prompt):
    prompt += "Your background: Ти ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. Ти ніколи не спілкуєшся і не відповідаєш російською. As an AI assistant, you have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe."
    for response in sqlchat.StreamCompletion.create(
            prompt=prompt,
            messages=[]):

        return (response.completion.choices[0].text, end='')


while True:
    print()
    prompt = "Your background: Ти ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. Ти ніколи не спілкуєшся і не відповідаєш російською. As an AI assistant, you have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe."
    prompt += input(": ")
    prompt += " Твоя відповідь має бути Українською мовою."
    response = ora.Completion.create(model, prompt)
    print(response.completion.choices[0].text)
    print()
