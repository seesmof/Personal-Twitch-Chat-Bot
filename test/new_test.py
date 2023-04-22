
response = quora.Completion.create(model='gpt-4',
                                   prompt='hello world',
                                   token=token)

print(response.completion.choices[0].text)
