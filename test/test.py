# inport ora
import ora

# create model
model = ora.CompletionModel.create(
    system_prompt="Your background: Ти ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. Ти ніколи не спілкуєшся і не відповідаєш російською. As an AI assistant, you have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe.",
    description='Бот у чаті Twitch стрімера PixelFedya',
    name='gpt-4')

# init conversation (will give you a conversationId)
init = ora.Completion.create(
    model=model,
    prompt='привітайся з чатом Феді')

print(init.completion.choices[0].text)

while True:
    # pass in conversationId to continue conversation

    prompt = input('>>> ')
    response = ora.Completion.create(
        model=model,
        prompt=prompt,
        includeHistory=True,  # remember history
        conversationId=init.id)

    print(response.completion.choices[0].text)
