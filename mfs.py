from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re
from vars import *
import ora
import phind


def split_long_gpt(input_string):
    num_substrings = len(input_string) // 475 + \
        (1 if len(input_string) % 475 > 0 else 0)
    substrings = [input_string[i * 475:(i + 1) * 475]
                  for i in range(num_substrings)]
    return substrings


async def send_split_gpt(ctx, message):
    substrings_list = split_long_gpt(message)
    for substring in substrings_list:
        await ctx.channel.send(substring)
        await asyncio.sleep(2)


def split_long_message(input_string):
    words = input_string.split()
    result = []
    for i in range(0, len(words), 10):
        result.append(" ".join(words[i:i+10]))
    return result


async def send_split_message(ctx, message):
    # split the given message
    substrings_list = split_long_message(message)
    # send each message
    for substring in substrings_list:
        await ctx.channel.send(substring)
        # add delay between each message
        await asyncio.sleep(2)


def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


def write_to_log(message, author, CHANNEL):
    # for handling current time
    now = datetime.now()
    # for handling the file name
    file_name = CHANNEL + "-log_" + now.strftime("%d-%m-%Y") + ".md"
    # for handling the file path
    file_path = os.path.join(log_dir, file_name)

    # open file with appropriate decoding
    with open(file_path, "a", encoding="utf-8") as log_file:
        # declare and output timestamp before message
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_file.write(timestamp)
        # output message with author name to log
        log_file.write(f"\n\n{author}: {message}\n")
        log_file.write(f"\n---\n\n")


#   <GENERATING MESSAGES>   #
def ora_ua(input_prompt, context):
    input_prompt += " Твоя відповідь має бути лише Українською мовою."
    input_model = ora.CompletionModel.create(
        system_prompt=context,
        description='AI Chat Bot',
        name='gpt-4')
    init = ora.Completion.create(
        model=input_model,
        prompt=input_prompt)
    return init.completion.choices[0].text


def ora_en(input_prompt, context):
    input_prompt += " Answer only in English."
    input_model = ora.CompletionModel.create(
        system_prompt=context,
        description='AI Chat Bot',
        name='gpt-4')
    init = ora.Completion.create(
        model=input_model,
        prompt=input_prompt)
    return init.completion.choices[0].text


def phind_ua(input_prompt):
    input_prompt += " Твоя відповідь має бути Українською мовою."

    # set cf_clearance cookie
    phind.cf_clearance = 'heguhSRBB9d0sjLvGbQECS8b80m2BQ31xEmk9ChshKI-1682268995-0-160'
    phind.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

    # normal completion
    result = phind.Completion.create(
        model='gpt-4',
        prompt=input_prompt,
        # create search (set actualSearch to False to disable internet)
        results=phind.Search.create(input_prompt, actualSearch=False),
        creative=False,
        detailed=False,
        codeContext='')  # up to 3000 chars of code

    return result.completion.choices[0].text


def phind_en(input_prompt):
    input_prompt += " Answer only in English."

    # set cf_clearance cookie
    phind.cf_clearance = 'heguhSRBB9d0sjLvGbQECS8b80m2BQ31xEmk9ChshKI-1682268995-0-160'
    phind.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

    # normal completion
    result = phind.Completion.create(
        model='gpt-4',
        prompt=input_prompt,
        # create search (set actualSearch to False to disable internet)
        results=phind.Search.create(input_prompt, actualSearch=False),
        creative=False,
        detailed=False,
        codeContext='')  # up to 3000 chars of code

    return result.completion.choices[0].text
