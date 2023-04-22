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
import ora

BOT_PREFIX = "!"
# CHANNEL = "seesmof"
CHANNEL = "k3ned1"

# initialize the bot with the necessary variables
bot = commands.Bot(
    irc_token=GPT_TMI_TOKEN,
    client_id=GPT_CLIENT_ID,
    nick=GPT_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

model = ora.CompletionModel.create(
    system_prompt=context_kenedy,
    description='Бот у чаті Twitch стрімера Кенеді',
    name='gpt-4')

init = ora.Completion.create(
    model=model,
    prompt='привітайся з чатом Феді')


def generate_ua(prompt):
    response = ora.Completion.create(
        model=model,
        prompt=prompt,
        includeHistory=False,  # remember history
        conversationId=init.id)
    return response.completion.choices[0].text


@ bot.event
async def event_ready():
    print(f"{GPT_BOT_NICK} is online at {CHANNEL}!")
    mfs.write_to_log(f"is online at {CHANNEL}!", GPT_BOT_NICK, CHANNEL)


@ bot.event
async def event_message(ctx):
    # handle situations with messages from a bot itself
    if ctx.author.name.lower() == GPT_BOT_NICK.lower():
        # log the message and move on
        print(f"\nBOT: {ctx.content}")
        mfs.write_to_log(ctx.content, GPT_BOT_NICK, CHANNEL)
        return

    # for handling ChatGPT requests from chat
    letters = ["@wuyodo"]
    # check if message contains bot mention
    if mfs.check_for_letters(ctx.content.lower(), letters):
        # check if the message is not from another bot
        if ctx.author.name.lower() == "k3ned1":
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
            output_text += generate_ua(input_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # output the generated message(s) to chat
            await mfs.send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(1)


if __name__ == "__main__":
    # launch bot
    bot.run()
