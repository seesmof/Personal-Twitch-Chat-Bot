from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re

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
