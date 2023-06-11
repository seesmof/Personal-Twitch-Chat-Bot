from vars import *
from mfs import *
import aiassist

question = input(": ")
req = aiassist.Completion.create(prompt=question)
answer = req["text"]
print(answer)
print()
