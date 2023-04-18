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

BOT_PREFIX = "!"
CHANNEL = "PixelFedya"
# CHANNEL = "seesmof"


bot = commands.Bot(
    irc_token=GPT_TMI_TOKEN,
    client_id=GPT_CLIENT_ID,
    nick=GPT_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@ bot.event
async def event_ready():
    print(f"{GPT_BOT_NICK} is online at {CHANNEL}!")
    mfs.write_to_log(f"is online at {CHANNEL}!", GPT_BOT_NICK, CHANNEL)


@ bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == GPT_BOT_NICK.lower():
        print(f"\nBOT: {ctx.content}")
        return

    letters = ["@wuyodo"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        if ctx.author.name.lower() != "pawrop":
            print("\nGenerating a message...")
            start_time = time.time()

            input_text = ctx.content.replace("@wuyodo", "")
            input_text = " ".join(input_text.split())

            output_text = "@" + ctx.author.name + ", "
            output_text += mfs.generate_ua(input_text, context_fedya)

            end_time = time.time()
            elapsed_time = end_time - start_time

            await mfs.send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(20)


if __name__ == "__main__":
    bot.run()
