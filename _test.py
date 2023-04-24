import sqlchat

input_text = input(': ')

for response in sqlchat.StreamCompletion.create(
        prompt=input_text,
        messages=[]):

    print(response.completion.choices[0].text, end='')
