import requests

# Make a GET request to the Twitch API endpoint for emotes
response = requests.get('https://api.twitch.tv/helix/chat/emotes')

# Extract the emote names from the response
emotes = [emote['name'] for emote in response.json()['data']]

# Format the emote names as a string
formatted_emotes = '", "'.join(emotes)

# Wrap the formatted emotes in brackets and backticks
formatted_emotes = f"[`\"{formatted_emotes}\"`]"

# Print the formatted emotes
print(formatted_emotes)
