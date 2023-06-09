from twitchio.ext import commands
from datetime import datetime
import openai
import os
import asyncio
import queue
import time
import requests
import re
from vars import *
import gpt4free
from gpt4free import Provider
from deep_translator import GoogleTranslator
from langdetect import detect
from Bard import Chatbot
import random
from notifypy import Notify


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
        await asyncio.sleep(6)


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
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"


def openai_generate(input_text, context):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": input_text}
        ],
        max_tokens=280,
        temperature=0.7,
    )
    output_text = response['choices'][0]['message']['content']
    return output_text


def gpt4free_ua(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='en').translate(input_text)
    response = gpt4free.Completion.create(
        Provider.You, prompt=input_prompt)
    response = GoogleTranslator(
        source='en', target='uk').translate(response)
    return response


def gpt4free_en(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='en').translate(input_text)
    response = gpt4free.Completion.create(
        Provider.You, prompt=input_prompt)
    return response


# Paste your Bard Token (check README.md for where to find yours)
token = "WwgpefTIfFTiaBOCfKpsSAU2lKZr_b3C1ogVkqYQpMqv8LRBRdRPIIpmvO9FDkKr51UUbg."
# Initialize Google Bard API
chatbot = Chatbot(token)


def bard_en(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='en').translate(input_text)
    response = chatbot.ask(input_prompt)
    return response['content']


def bard_ua(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='en').translate(input_text)
    response = chatbot.ask(input_prompt)
    response = GoogleTranslator(
        source='en', target='uk').translate(response)
    return response['content']


def generate_ai_message(message, author):
    print("\nGenerating a message...\n")
    start_time = time.time()

    input_text = message.replace("@piprly", "")
    input_text = message.replace("@wuyodo", "")
    input_text = " ".join(input_text.split())

    output_text = ""  # declare the variable here

    if detect(input_text) == "uk" or detect(input_text) == "ru":
        print("Language is Ukrainian")
        try:
            print("Generating with GPT4Free")
            output_text += gpt4free_ua(input_text)
        except:
            try:
                print("Generating with Bard")
                output_text += bard_ua(input_text)
            except:
                print(
                    f"\n{author} got an error while trying to generate message!\nPrompt: {message}\n")
                output_text += random.choice(error_ua)
                notification = Notify()
                notification.audio = error_sound_path
                notification.send()
    else:
        print("Language is English")
        try:
            print("Generating with GPT4Free")
            output_text += gpt4free_en(input_text)
        except:
            try:
                print("Generating with Bard")
                output_text += bard_en(input_text)
            except:
                print(
                    f"\n{author} got an error while trying to generate message!\nPrompt: {message}\n")
                output_text += random.choice(error_en)
                notification = Notify()
                notification.audio = error_sound_path
                notification.send()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nGenerated in {elapsed_time:.2f} seconds")
    return output_text
