from vars import *
from mfs import *
from gpt4free import usesless


def useless_ua(input_text):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDczMzEsImlhdCI6MTY4NjQ5Mjc3MiwiZXhwIjoxNzE4MDUwMzcyfQ.dZdg4CdyS4HuJUD2NSnYQYJCr2o9b5cdIhEo6W5KXGA"
    message_id = ''
    input_prompt = GoogleTranslator(
        source='auto', target='uk').translate(input_text)
    req = usesless.Completion.create(
        prompt=input_text, parentMessageId=message_id, token=token)
    response = req['text']
    return response


inputtext = input(": ")
print(useless_ua(inputtext))
