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
            output_text = gpt4free_ua(input_prompt)
        else:
            output_text = gpt4free_en(input_prompt)
        print(output_text)


if __name__ == "__main__":
    main()
