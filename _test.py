import forefront
import vars


# create an account
token = forefront.Account.create(logging=True)


def generate(input_prompt: str) -> str:
    response = forefront.StreamingCompletion.create(
        token=token, prompt=input_prompt, model='gpt-4')
    return response.completion.choices[0].text


inputstr = input(": ")
out = generate(inputstr)
print(out)
