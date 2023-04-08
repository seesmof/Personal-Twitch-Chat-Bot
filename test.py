def split_string(string):
    words = string.split()
    # create a list to hold the resulting strings
    result = []
    # loop through the words, adding each group of six to the result list
    for i in range(0, len(words), 6):
        result.append(" ".join(words[i:i+6]))
    return result


string = "This is a test string that we will use to demonstrate the function."
result = split_string(string)
print(result)
