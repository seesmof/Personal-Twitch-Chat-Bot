# import quora (poe) package
import quora

# create account
# make sure to set enable_bot_creation to True
token = quora.Account.create(logging=True, enable_bot_creation=False)

response = quora.Completion.create(model='gpt-4',
                                   prompt='hello world',
                                   token=token)

print(response.completion.choices[0].text)
