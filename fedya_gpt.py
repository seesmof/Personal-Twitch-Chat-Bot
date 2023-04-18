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


@ bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{BOT_NICK} is online at {CHANNEL}!")
    # log it
    mfs.write_to_log(f"is online at {CHANNEL}!", BOT_NICK, CHANNEL)


@ bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BOT_NICK.lower():
        print(f"\nBOT: {ctx.content}")
        mfs.write_to_log(ctx.content, BOT_NICK, CHANNEL)
        return

    letters = ["@wuyodo"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        if ctx.author.name.lower() != "pawrop":
            print("\nGenerating a message...")
            start_time = time.time()

            input_text = ctx.content.replace("@wuyodo", "")
            input_text = " ".join(input_text.split())

            output_text = "@" + ctx.author.name + ", "
            output_text += mfs.generate(input_text, context_fedya)

            end_time = time.time()
            elapsed_time = end_time - start_time

            await mfs.send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(20)


if __name__ == "__main__":
    bot.run()
