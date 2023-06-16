import requests

letters = "f h n s u i s"
response = requests.get(
    f"https://wordfinder.yourdictionary.com/unscramble/{letters}")
words = response.json()["words"]
print(words)
