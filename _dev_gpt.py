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
import pyautogui
import random

BOT_PREFIX = "!"
CHANNEL = "seesmof"
bot = commands.Bot(
    irc_token=GPT_TMI_TOKEN,
    client_id=GPT_CLIENT_ID,
    nick=GPT_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)
chat = []


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
    if mfs.check_for_letters(ctx.content.lower(), letters) and ctx.author.name.lower() != "pawrop":
        all_good = True
        print("\nGenerating a message...")
        start_time = time.time()

        input_text = ctx.content.replace("@wuyodo", "")
        input_text = " ".join(input_text.split())
        output_text = "@" + ctx.author.name + ", "
        try:
            output_text += mfs.ora_ua(input_text, context_fedya)
        except:
            output_text += "Повідомлення не було згенеровано." + \
                random.choice(mfs.error_ua)
            all_good = False

        end_time = time.time()
        elapsed_time = end_time - start_time
        await mfs.send_split_gpt(ctx, output_text)
        print(f"\nGenerated in {elapsed_time:.2f} seconds")
        if all_good:
            mfs.write_to_log(
                f"Generated in {elapsed_time:.2f} seconds", GPT_BOT_NICK, CHANNEL)
        else:
            mfs.write_to_log(
                f"Повідомлення не було згенеровано.", GPT_BOT_NICK, CHANNEL)
            pyautogui.alert("No message was generated, check it out. Most likely a problem on service side",
                            "ERROR: No message generated", timeout=None)
    await asyncio.sleep(20)


if __name__ == "__main__":
    bot.run()
