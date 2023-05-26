import gpt4free
from gpt4free import Provider
from deep_translator import GoogleTranslator

general_prompt = "Imagine you are a personal AI assistant, which has three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe and increase understanding in the universe. "

def make_api_call(input_text):
    response = gpt4free.Completion.create(
        Provider.You, prompt=input_text)
    return response

def break_down_prompt(input_text):
    input_text += f"Please identify the key words or phrases in the prompt. Output them in the following format: \"key1\", \"key2\", ..."
    print(f"\n{input_text}\n")
    result = make_api_call(input_text)
    return result


# def break_down_keyword(keywords):
    

def main():
    global general_prompt
    initial_prompt = input(": ")
    general_prompt += f"Your goal right now is to solve this problem: \"{initial_prompt}\". The phrase in brackets is your prompt you will be working with, please keep that in mind. "
    
    keywords = break_down_prompt(general_prompt)

main()