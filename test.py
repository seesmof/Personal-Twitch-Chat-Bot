import sqlchat

prompt = "Your background: Ти ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. Ти ніколи не спілкуєшся і не відповідаєш російською. As an AI assistant, you have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe."
prompt += input(": ")
prompt += " Твоя відповідь має бути Українською мовою."
for response in sqlchat.StreamCompletion.create(
        prompt=prompt,
        messages=[]):

    print(response.completion.choices[0].text, end='')
