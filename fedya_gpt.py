# include necessary libraries/files
from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re
import mfs

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
    if mfs.check_for_letters(ctx.content.lower(), letters):
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
            output_text += mfs.gen_fedya(input_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # output the generated message(s) to chat
            await mfs.send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(20)


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
