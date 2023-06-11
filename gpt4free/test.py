import aiassist
from gpt4free import aicolors

question = input(": ")
req = aiassist.Completion.create(prompt=question)
answer = req["text"]
print(answer)
print()

req = aicolors.Completion.create(prompt=question)
print(req)
print()
