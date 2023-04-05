# import the llama language model
from llama_language_model import LlamaModel

# create an instance of the model
model = LlamaModel()

# take input from the user
user_input = input("Enter your input: ")

# generate output from the llama language model
output = model.generate_text(user_input)

# print the output on the screen
print(output)
