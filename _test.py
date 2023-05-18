import gpt4free
from gpt4free import Provider

in_text = input(": ")

response = gpt4free.Completion.create(Provider.You, prompt=in_text)
print(response)