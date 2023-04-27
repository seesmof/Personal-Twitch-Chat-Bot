import forefront
import vars

# create an account
token = forefront.Account.create(logging=True)

inputstr = input(": ")

# get a response
for response in forefront.StreamingCompletion.create(token=token,
                                                     prompt=inputstr, model='gpt-4'):

    print(response.completion.choices[0].text, end='')
