import forefront
import vars


# create an account
token = forefront.Account.create(logging=True)


def ai_response(input_prompt):
    response = forefront.StreamingCompletion.create(
        token=token, prompt=input_prompt, model='gpt-4')
    return response.completion.choices[0].text


inputstr = input(": ")
out = ai_response(inputstr)
print(out)

for response in forefront.StreamingCompletion.create(token=token,
                                                     prompt=inputstr, model='gpt-4'):
    print(response.completion.choices[0].text, end='')
