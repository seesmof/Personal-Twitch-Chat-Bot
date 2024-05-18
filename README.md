# Twitch Chatbot with ChatGPT

This project is a Twitch chatbot that uses OpenAI's GPT-3.5 model to generate responses to user queries. The bot can respond to various types of input, from simple questions to more complex requests.

## Installation

To run this bot, you will need to install the following libraries:

- `pathlib`
- `dotenv`
- `twitchio`
- `playsound`
- `datetime`
- `openai`

You will also need to create a `.env` file with the following content:

```lua
TMI_TOKEN=<your Twitch bot's token>
CLIENT_ID=<your Twitch bot's client ID>
log_dir=<folder path for log files>
```

Additionally, you will need to provide your OpenAI API key and the name of the GPT-3.5 model you want to use.

## Usage

To start the bot, run the `twitch_chatbot.py` file. The bot will then be ready to respond to user messages in the Twitch chat.

The bot will respond to messages that begin with "@wuyodo". If a user sends a message without this prefix, the bot will not respond.

The bot will greet users once per day. If a user sends a message multiple times in a day, the bot will not greet them again.

The bot can also respond to various types of input, from simple questions to more complex requests. To make a request to the bot, type "@wuyodo" followed by your query.

## Emotes

The bot can also respond with a variety of emotes. Here are some examples of the emotes the bot can use:

- Hand gestures: ✋, ✌️, 👐, 👋, 🤚, 🤙
- Nose: 👃, 🐽, 👃🏻, 👃🏿, 👃🏽, 👃🏼, 👃🏾
- Tongue: 😛, 😜, 😝, 😋
- Shy: 🤗, 👐, 🤭, 😄, 🥰, 😼, 😙, 😍, 😻, 😅
- Laugh: 🍑, 🤣, 😂, 😹, 😆, 🙈
- Kiss: 👄, 💋, 😘, 😚, 😙, 😽

## Contributing

If you would like to contribute to this project, please open a pull request.
