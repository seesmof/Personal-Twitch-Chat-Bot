import gpt4free
from gpt4free import Provider, quora, forefront

token = forefront.Account.create(logging=False)
response = gpt4free.Completion.create(
    Provider.ForeFront, prompt='Write a poem on Lionel Messi', model='gpt-4', token=token
)
print(response)
print(f'END')
