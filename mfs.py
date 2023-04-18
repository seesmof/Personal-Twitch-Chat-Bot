from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re
from vars import *


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


def generate_ua(input_text, context):
    input_text += " Твоя відповідь має бути Українською мовою."
    url = "https://www.phind.com/api/infer/creative"
    data = {
        "question": input_text,
        "codeContext": context,
        "options": {
            "skill": "advanced",
            "date": "14/04/2023",
            "language": "uk-UA",
            "detailed": False,
            "creative": False,
            "concise": True,
            "expert": True
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
    if response.status_code != 200:
        return "Whoops... Something went wrong. Try again later"

    data = response.text
    text = data.replace("data: ", "")
    text = text.replace("\n ", " ")
    text = f'''{text}'''
    text = text.replace('''\r\n\r\n''', "")
    text = text.replace('''\r\n\r''', " ")
    text = text.replace('''`''', "")
    text = text.replace('''*''', "")
    return text


def generate_ua(input_text, context):
    input_text += " Твоя відповідь має бути Українською мовою."
    url = "https://www.phind.com/api/infer/creative"
    data = {
        "question": input_text,
        "codeContext": context,
        "options": {
            "skill": "advanced",
            "date": "14/04/2023",
            "language": "uk-UA",
            "detailed": False,
            "creative": False,
            "concise": True,
            "expert": True
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
    if response.status_code != 200:
        return "Whoops... Something went wrong. Try again later"

    data = response.text
    text = data.replace("data: ", "")
    text = text.replace("\n ", " ")
    text = f'''{text}'''
    text = text.replace('''\r\n\r\n''', "")
    text = text.replace('''\r\n\r''', " ")
    text = text.replace('''`''', "")
    text = text.replace('''*''', "")
    return text


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
