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
            try:
                output_text = gpt4free_ua(input_prompt)
            except:
                output_text = random.choice(error_ua)
        else:
            try:
                output_text = gpt4free_en(input_prompt)
            except:
                output_text = random.choice(error_en)


if __name__ == "__main__":
    main()
