import forefront

token = forefront.Account.create(logging=False)
for response in forefront.StreamingCompletion.create(token=token,
                                                     prompt='hello world', model='gpt-4'):
    print(response.completion.choices[0].text, end='')
print("")
