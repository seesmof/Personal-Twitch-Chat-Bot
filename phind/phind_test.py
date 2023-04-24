import phind

# set cf_clearance cookie
phind.cf_clearance = 'heguhSRBB9d0sjLvGbQECS8b80m2BQ31xEmk9ChshKI-1682268995-0-160'
phind.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

prompt = 'hello world'

# normal completion
result = phind.Completion.create(
    model='gpt-4',
    prompt=prompt,
    # create search (set actualSearch to False to disable internet)
    results=phind.Search.create(prompt, actualSearch=False),
    creative=False,
    detailed=False,
    codeContext='')  # up to 3000 chars of code

print(result.completion.choices[0].text)

prompt = 'who won the quatar world cup'

# help needed: not getting newlines from the stream, please submit a PR if you know how to fix this
# stream completion
for result in phind.StreamingCompletion.create(
    model='gpt-3.5',
    prompt=prompt,
    # create search (set actualSearch to False to disable internet)
    results=phind.Search.create(prompt, actualSearch=True),
    creative=False,
    detailed=False,
        codeContext=''):  # up to 3000 chars of code

    print(result.completion.choices[0].text, end='', flush=True)
