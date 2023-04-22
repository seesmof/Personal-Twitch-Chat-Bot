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


def generate_ua(input_text, context):
    input_text = input("\nВведіть текст: ")
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
