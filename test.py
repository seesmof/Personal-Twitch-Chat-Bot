import phind

prompt = 'who won the quatar world cup'

# help needed: not getting newlines from the stream, please submit a PR if you know how to fix this
# stream completion
for result in phind.StreamingCompletion.create(
        model='gpt-4',
        prompt=prompt,
        # create search (set actualSearch to False to disable internet)
        results=phind.Search.create(prompt, actualSearch=True),
        creative=False,
        detailed=False,
        codeContext=''):  # up to 3000 chars of code

    print(result.completion.choices[0].text, end='', flush=True)

# normal completion
result = phind.Completion.create(
    model='gpt-4',
    prompt=prompt,
    # create search (set actualSearch to False to disable internet)
    results=phind.Search.create(prompt, actualSearch=True),
    creative=False,
    detailed=False,
    codeContext='')  # up to 3000 chars of code

print(result.completion.choices[0].text)
