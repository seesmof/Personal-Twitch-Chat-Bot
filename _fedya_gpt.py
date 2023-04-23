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
CHANNEL = "PixelFedya"
# CHANNEL = "seesmof"


bot = commands.Bot(
    irc_token=GPT_TMI_TOKEN,
    client_id=GPT_CLIENT_ID,
    nick=GPT_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

gpt4_chatbot_ids = ['b8b12eaa-5d47-44d3-92a6-4d706f2bcacf', 'fbe53266-673c-4b70-9d2d-d247785ccd91', 'bd5781cf-727a-45e9-80fd-a3cfce1350c6', '993a0102-d397-47f6-98c3-2587f2c9ec3a', 'ae5c524e-d025-478b-ad46-8843a5745261', 'cc510743-e4ab-485e-9191-76960ecb6040', 'a5cd2481-8e24-4938-aa25-8e26d6233390', '6bca5930-2aa1-4bf4-96a7-bea4d32dcdac', '884a5f2b-47a2-47a5-9e0f-851bbe76b57c', 'd5f3c491-0e74-4ef7-bdca-b7d27c59e6b3', 'd72e83f6-ef4e-4702-844f-cf4bd432eef7',
                    '6e80b170-11ed-4f1a-b992-fd04d7a9e78c', '8ef52d68-1b01-466f-bfbf-f25c13ff4a72', 'd0674e11-f22e-406b-98bc-c1ba8564f749', 'a051381d-6530-463f-be68-020afddf6a8f', '99c0afa1-9e32-4566-8909-f4ef9ac06226', '1be65282-9c59-4a96-99f8-d225059d9001', 'dba16bd8-5785-4248-a8e9-b5d1ecbfdd60', '1731450d-3226-42d0-b41c-4129fe009524', '8e74635d-000e-4819-ab2c-4e986b7a0f48', 'afe7ed01-c1ac-4129-9c71-2ca7f3800b30', 'e374c37a-8c44-4f0e-9e9f-1ad4609f24f5']
chatbot_id = gpt4_chatbot_ids[0]
model = ora.CompletionModel.load(chatbot_id, 'gpt-4')


def generate_ua(prompt):
    prompt += context_fedya
    prompt += " Твоя відповідь має бути Українською мовою."
    response = ora.Completion.create(model, prompt)
    text = response.completion.choices[0].text
    text = text.replace("*", "")
    return text


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
            output_text += generate_ua(input_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            await mfs.send_split_gpt(ctx, output_text)
            print(f"\nGenerated in {elapsed_time:.2f} seconds")
    await asyncio.sleep(20)


if __name__ == "__main__":
    bot.run()
