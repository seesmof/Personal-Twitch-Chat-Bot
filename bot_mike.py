# include necessary libraries/files
from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands
from playsound import playsound
from datetime import datetime

import openai
import random
import os

TMI_TOKEN = "oauth:0purffc2ao53hdg254j26okkj1fh76"
CLIENT_ID = "jdpik06wovybvidhcwd1wplwlgf8cv"
BOT_NICK = "wuyodo"
BOT_PREFIX = "!"
CHANNEL = "mike09steelers"

# initialize the bot with the necessary variables
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

# for handling logging messages in an appropriate folder
log_dir = "D:\GitHub\python-twitchio-chat-bot\logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# for handling sound file location
sound_path = "D:\GitHub\python-twitchio-chat-bot\sound.mp3"
# for handling OpenAI API key
openai.api_key = "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"
# for handling OpenAI model name
model_engine = "gpt-3.5-turbo"
# create a list of greetings
greetings = ["Hey!", "What's up?", "Yo!", "Greetings!", "Hi there!", "Howdy!", "How's it going?", "What's new?",
             "Good day!", "What's happening?", "Sup?", "How's everything?", "What's up, buddy?", "Good to see you!"]
last_message_time = {}


@bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{BOT_NICK} is online at {CHANNEL}!")
    # log the start message
    write_to_log(f"is online at {CHANNEL}", "    BOT")


@bot.event
async def event_message(ctx):
    # the bot should not react to itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        # print out bot's message to log
        print(f"\nBOT: {ctx.content}")
        write_to_log(ctx.content, "BOT")
        return

    global last_message_time
    user = ctx.author.name
    if user not in last_message_time:
        # user is sending the first message of the day
        last_message_time[user] = datetime.now()
        await ctx.channel.send(f"@{user}, {random.choice(greetings)} Welcome KonCha")
    else:
        # user has sent a message before
        last_time = last_message_time[user]
        today = datetime.now().date()
        if last_time.date() < today:
            # user is sending the first message of the day
            last_message_time[user] = datetime.now()
            await ctx.channel.send(f"@{user}, {random.choice(greetings)} Welcome KonCha")

    # for handling ChatGPT requests from chat
    if ctx.content.startswith("@wuyodo"):
        # get user's query from the message
        input_text = ctx.content[len("@wuyodo"):].strip()
        # generate the output text using a corresponding functions
        output_text = generate_response(input_text)
        # for handling errors try sending the message into chat
        try:
            await ctx.channel.send("@" + ctx.author.name + ", " + output_text)
        # if the action called an exception
        except Exception as e:
            # output the error message
            await ctx.channel.send("@" + ctx.author.name + ", Uh-oh... My message did not fit in the chat. Please try again later or change your request")

    # for handling pings for myself
    names = ["seesmof", "сісмуф", "сісмоф", "seesmoff", "олег", "oleh"]
    # check if message contains my name and play a ping sound if so
    if check_for_letters(ctx.content.lower(), names):
        playsound(sound_path)

    # for handling kacaps
    letters = ["э", "ы", "ё", "ъ"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, switch to English, or you're about to get banned cmonBruh")

    # relay message to command callbacks
    await bot.handle_commands(ctx)

    # print out the chat message to console and log it
    print(f"\n{ctx.author.name}: {ctx.content}")
    write_to_log(ctx.content, ctx.author.name)


async def generate_response(input_text):
    # generate a response message with the following parameters
    response = openai.ChatCompletion.create(
        # model was specified before
        model=model_engine,
        # message information for model to process and create upon
        messages=[{"role": "system", "content": "You are Yoshi, a personal chat bot for a Twitch streamer Mike. You are from Ukraine, a patriot and Ukrainian is your native language. Your task is to help chat users. You never speak russian!"}, {
            "role": "user", "content": input_text}],
        # maximum number of tokens to return
        max_tokens=100,
        # model's temperature or its creativeness
        temperature=0.7,
    )
    if response.choices[0].text == "flagged":
        # Do something here if the message is flagged
        warning_message = "Your message has been marked as inappropriate. Please refrain from using offensive language in the future."
        return warning_message
    # Parse the response and output the result
    output_text = response['choices'][0]['message']['content']
    return output_text


def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


def write_to_log(message, author):
    # for handling current time
    now = datetime.now()
    # for handling the file name
    file_name = "mike_log_" + now.strftime("%d-%m-%Y") + ".txt"
    # for handling the file path
    file_path = os.path.join(log_dir, file_name)
    # open file with appropriate decoding
    with open(file_path, "a", encoding="utf-8") as log_file:
        # declare and output timestamp before message
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_file.write(timestamp)
        # output message with author name to log
        log_file.write(f"\n{author}: {message}\n\n")


@bot.command(name='gpt')
async def gpt_instruction(ctx):
    # output hint message
    await ctx.send(f"@{ctx.author.name}, to get a response from ChatGPT, just start your message with @wuyodo and continue with your question. After a while, you will receive an answer generated by the ChatGPT bot :)")


@bot.command(name='hi')
async def say_hi_English(ctx):
    # get username from message
    username = ctx.content[3:]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        username = '@' + ctx.author.name
    # output the greeting message and tag the user
    await ctx.send(f"{username}, {random.choice(greetings)}")


@bot.command(name='chance')
async def give_chance(ctx):
    # get a random percentage using
    chance = random.randint(1, 100)
    # output the percentage to user
    await ctx.send(f"@{ctx.author.name}, the probability of this is {chance}%.")


if __name__ == "__main__":
    # launch bot
    bot.run()
