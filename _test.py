from gpt4free import deepai

def list_of_vacation_destinations():
  results = []
  for chunk in deepai.Completion.create("Write a list of possible vacation destinations:"):
    results.append(chunk)
  return results


destinations = list_of_vacation_destinations()