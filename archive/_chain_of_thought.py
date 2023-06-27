import gpt4free
from gpt4free import Provider
from deep_translator import GoogleTranslator

general_prompt = "Imagine you are a personal AI assistant, which has three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe and increase understanding in the universe. "

def make_api_call(input_text):
    response = gpt4free.Completion.create(
        Provider.You, prompt=input_text)
    return response

def break_down_prompt(input_text):
    input_text += f"Please identify the key words or phrases in the prompt. Output them in the following format: \"key1\", \"key2\", ... Make sure the output is not too long."
    result = make_api_call(input_text)
    return result


def break_down_keyword(input_text):
    input_text += f"Please break each key word or phrase down into a smaller step. Output them in the following format: \"step1\", \"step2\", ... Make sure the output is not too long."
    result = make_api_call(input_text)
    return result


def identify_list_of_solutions(input_text):
    input_text += f"Please identify a list of possible solutions to your goal from given steps. Output them in the following format: \"solution1\", \"solution2\", ... Make sure the output is not too long."
    result = make_api_call(input_text)
    return result

def choose_best_solution(input_text):
    input_text += f"Please choose the best solution from the list of possible solutions. Output it in the following format: \"best_solution\". Make sure the output is not too long."
    result = make_api_call(input_text)
    return result

def implement_solution(input_text):
    input_text += f"Please implement the best solution. Output your final answer given all the information you have. Make sure it is the absolute best solution and it is what the person is asking for. Make sure the output is not too long."
    result = make_api_call(input_text)
    return result

def main():
    global general_prompt
    initial_prompt = input(": ")
    general_prompt += f"Your goal right now is to solve this problem: \"{initial_prompt}\". The phrase in brackets is your prompt you will be working with, please keep that in mind.\n\n"
    keywords = break_down_prompt(general_prompt)
    general_prompt += f"Keywords: \"{keywords}\"\n\n"
    steps_from_keywords = break_down_keyword(general_prompt)
    general_prompt += f"Steps: \"{steps_from_keywords}\"\n\n"
    list_of_solutions = identify_list_of_solutions(general_prompt)
    general_prompt += f"Possible solutions: \"{list_of_solutions}\"\n\n"
    best_solution = choose_best_solution(general_prompt)
    general_prompt += f"Best solution: \"{best_solution}\"\n\n"
    final_solution = implement_solution(general_prompt)
    print(final_solution)


main()