from twitchio.ext import commands
from datetime import datetime
import openai
import os
import asyncio
import time
import requests
import re
from mfs import *
from vars import *
import pyautogui
import random
from langdetect import detect


def main():
    while True:
        input_prompt = input(": ")
        output_text = ""
        if detect(input_prompt) == "uk":
            print(detect(input_prompt))
            try:
                print("UA: Trying GPT4Free")
                output_text = gpt4free_ua(input_prompt)
                error_text = "unable to fetch response"
                if check_for_letters(output_text.lower(), error_text):
                    print("UA: Trying Bard")
                    try:
                        output_text = bard_ua(input_prompt)
                    except:
                        output_text = random.choice(error_ua)
            except:
                output_text = random.choice(error_ua)
        else:
            print(detect(input_prompt))
            try:
                print("EN: Trying GPT4Free")
                output_text = gpt4free_en(input_prompt)
                error_text = "unable to fetch response"
                if check_for_letters(output_text.lower(), error_text):
                    print("EN: Trying Bard")
                    try:
                        output_text = bard_en(input_prompt)
                    except:
                        output_text = random.choice(error_en)
            except:
                output_text = random.choice(error_en)
        print(output_text)


if __name__ == "__main__":
    main()
