import forefront
import vars

# create an account
token = forefront.Account.create(logging=True)

inputstr = "Your background: Ти ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. Ти ніколи не спілкуєшся і не відповідаєш російською. As an AI assistant, you have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe."
inputstr += input(": ")

# get a response
for response in forefront.StreamingCompletion.create(token=token,
                                                     prompt=inputstr, model='gpt-4'):

    print(response.completion.choices[0].text, end='')
