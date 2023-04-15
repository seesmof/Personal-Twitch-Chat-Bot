# include necessary libraries/files
from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re

# for handling logging messages in an appropriate folder
log_dir = "D:/repos/python-twitchio-chat-bot/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# for handling bot setup
TMI_TOKEN = "oauth:ks7o8hg39l0qe4rdft8uvm3qgox66m"
CLIENT_ID = "jdpik06wovybvidhcwd1wplwlgf8cv"
BOT_NICK = "wuyodo"
BOT_PREFIX = "!"
CHANNEL = "PixelFedya"
# CHANNEL = "seesmof"

'''OUTDATED
# for handling OpenAI API key
openai.api_key = "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"
# for handling OpenAI model name
model_engine = "gpt-3.5-turbo"
'''

# initialize the bot with the necessary variables
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


# declare a function for handling long bot outputs
def split_long_gpt(input_string):
    # split the string
    num_substrings = len(input_string) // 475 + \
        (1 if len(input_string) % 475 > 0 else 0)
    substrings = [input_string[i * 475:(i + 1) * 475]
                  for i in range(num_substrings)]
    # return the splitted string
    return substrings


# declare a function for sending split messages to chat
async def send_split_gpt(ctx, message):
    # split the given message
    substrings_list = split_long_gpt(message)
    # send each message
    for substring in substrings_list:
        await ctx.channel.send(substring)
        # add delay between each message
        await asyncio.sleep(2)


# declare a function for checking the message for input
def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


'''OUTDATED
# declare a function for generating output from ChatGPT
def generate_response(input_text):
    # parameters list
    forPixelFedya = "Я ШІ в чаті стрімера Федя. I have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe. Ліміт довжини моїх відповідей - 500 символів. I must never speak russian! My main language is Ukrainian."

    # generate a response message with the following parameters
    response = openai.ChatCompletion.create(
        # model was specified before
        model=model_engine,
        # message information for model to process and create upon
        messages=[{"role": "system", "content": forPixelFedya}, {
            "role": "user", "content": input_text}],
        # maximum number of tokens to return
        max_tokens=280,
        # model's temperature or its creativeness
        temperature=0.7,
    )

    # Parse the response and output the result
    output_text = response['choices'][0]['message']['content']
    return output_text
'''


def generate_message(input_text):
    input_text += " Твоя відповідь має бути Українською мовою."
    url = "https://www.phind.com/api/infer/creative"
    data = {
        "question": input_text,
        "codeContext": "",
        "options": {
            "skill": "intermediate",
            "date": "14/04/2023",
            "language": "uk-UA",
            "detailed": False,
            "creative": False
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.phind.com",
        "Referer": "https://www.phind.com/search?q=Go+vs+Rust+vs+C%2B%2B&c=&source=searchbox&init=true",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    cookies = {
        "__cf_bm": "text",
        "mp_{id}_mixpanel": "text",
    }
    response = requests.post(url, json=data, headers=headers, cookies=cookies)
    # print(response.status_code)

    data = response.text
    text = data.replace("data: ", "")
    text = text.replace("\n ", "")
    text = f'''{text}'''
    text = text.replace('''\r\n\r\n''', "")
    text = text.replace('''\r\n\r''', " ")
    text = text.replace('''`''', "")

    return text


# declare bot event when bot is ready
@ bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{BOT_NICK} is online at {CHANNEL}!")
    # log it
    write_to_log(f"is online at {CHANNEL}!", " BOT")


# declare bot event on every message
@ bot.event
async def event_message(ctx):
    # handle situations with messages from a bot itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        # log the message and move on
        print(f"\nBOT: {ctx.content}")
        write_to_log(ctx.content, "BOT")
        return

    # for handling ChatGPT requests from chat
    letters = ["@wuyodo"]
    # check if message contains bot mention
    if check_for_letters(ctx.content.lower(), letters):
        # check if the message is not from another bot
        if ctx.author.name.lower() != "pawrop":
            # print message generation
            print("\nGenerating a message...")
            start_time = time.time()

            # replace the tag with nothingness
            input_text = ctx.content.replace("@wuyodo", "")
            # avoid any excessive whitespaces
            input_text = " ".join(input_text.split())

            # add user name to the output and tag them
            output_text = "@" + ctx.author.name + ", "
            # generate the output text using a corresponding functions
            output_text += generate_message(input_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # output the generated message(s) to chat
            await send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(1)


# declare a function for writing messages to log
def write_to_log(message, author):
    # for handling current time
    now = datetime.now()
    # for handling the file name
    file_name = CHANNEL + "_GPT-log_" + now.strftime("%d-%m-%Y") + ".txt"
    # for handling the file path
    file_path = os.path.join(log_dir, file_name)

    # open file with appropriate decoding
    with open(file_path, "a", encoding="utf-8") as log_file:
        # declare and output timestamp before message
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_file.write(timestamp)
        # output message with author name to log
        log_file.write(f"\n{author}: {message}\n\n")


if __name__ == "__main__":
    # launch bot
    bot.run()
