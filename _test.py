from vars import *
from mfs import *
from gpt4free import usesless


input_text = input(": ")
output_text = generate_ai_message(
    input_text, "seesmof")
output_text = split_long_gpt(output_text)
for substr in output_text:
    print(f"{substr} @seesmof")
