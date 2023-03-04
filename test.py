# Pay attention to check that your OpenAI version must be v0.27.0 or above
import openai

# First, you need to set up your API key
openai.api_key = "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"

# Then, you can call the "gpt-3.5-turbo" model
model_engine = "gpt-3.5-turbo"

# set your input text
input_text = input("Input: ")

# Send an API request and get a response, note that the interface and parameters have changed compared to the old model
response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[{"role": "system", "content": "Ти доброзичливий чат-бот Твіч стрімера Піксельний Федя. Твоя задача - допомагати користувачам чата з будь-якими питаннями, які в них можуть виникнути. Я спілкуюсь лише Українською та Англійською мовами. Якщо користувач звертається до тебе російською, реагуй виключно негативно і відмовляйся спілкуватись з ним."}, {
        "role": "user", "content": input_text}]
)

# response will get a json message with a structure like this
# {
#  'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
#  'object': 'chat.completion',
#  'created': 1677649420,
#  'model': 'gpt-3.5-turbo',
#  'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
#  'choices': [
#    {
#     'message': {
#       'role': 'assistant',
#       'content': 'The 2014 FIFA World Cup was held in Brazil.'},
#     'finish_reason': 'stop',
#     'index': 0
#    }
#   ]
# }

# Parse the response and output the result
output_text = response['choices'][0]['message']['content']
print("ChatGPT API reply:", output_text)
