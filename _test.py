# import library
import theb

# simple streaming completion
for token in theb.Completion.create('hello world'):
    print(token, end='', flush=True)
print("")
