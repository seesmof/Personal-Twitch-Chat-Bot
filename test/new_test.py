import quora
token = quora.Account.create(logging=True, enable_bot_creation=True)
response = quora.Completion.create(model='gpt-4',
                                   prompt='hi, who are you?',
                                   token=token)

print(response.completion.choices[0].text)
