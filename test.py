import cocalc
import you

response = you.Completion.create(
    prompt="Hello World",  # Required
    system_prompt="You are ChatGPT"  # Optional
)

print(response)  # Just text response
