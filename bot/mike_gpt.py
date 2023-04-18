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
from vars import *

# for handling logging messages in an appropriate folder
log_dir = "D:/repos/python-twitchio-chat-bot/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# for handling bot setup
TMI_TOKEN = "oauth:ks7o8hg39l0qe4rdft8uvm3qgox66m"
CLIENT_ID = "jdpik06wovybvidhcwd1wplwlgf8cv"
BOT_NICK = "wuyodo"
BOT_PREFIX = "!"
CHANNEL = "mike09steelers"

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
    await asyncio.sleep(30)


if __name__ == "__main__":
    # launch bot
    bot.run()
