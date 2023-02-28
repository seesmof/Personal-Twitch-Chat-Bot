import os
import json

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands

import time
import asyncio
import openai
import math
import random

# Set up the OpenAI API key and model ID
openai.api_key = "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"
model_id = "text-davinci-003"


def generate_response(input_text):
    response = openai.Completion.create(
        engine=model_id,
        prompt=input_text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    text = response.choices[0].text.strip()
    return text


def check_for_letters(text, letters):
    for letter in letters:
        if letter in text:
            return True
    return False


dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

# credentials
TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CHANNEL = os.environ.get('CHANNEL')

JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@bot.event
async def event_ready():
    print(f"{BOT_NICK} is online at {CHANNEL}!")


@bot.event
async def event_message(ctx):
    # the bot should not react to itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        print(f"\nBOT: {ctx.content}")
        return

    if ctx.content.startswith("@wuyodo"):
        # Strip out the "!гпт" command and pass the remaining text to the GPT-3 model
        input_text = ctx.content[len("@wuyodo"):].strip()
        input_text += " Дай просту відповідь Українською"
        output_text = generate_response(input_text)
        try:
            await ctx.channel.send("@" + ctx.author.name + ", " + output_text)
        except Exception as e:
            await ctx.channel.send("@" + ctx.author.name + ", Ой-ой... Моє повідомлення не вмістилось в чат. Спробуйте трохи пізніши або змініть свій запит.")

    # relay message to command callbacks
    await bot.handle_commands(ctx)

    print(f"\n{ctx.author.name}: {ctx.content}")

    text = ctx.content
    letters = ["э", "ы", "ё", "ъ"]
    if check_for_letters(text, letters):
        print("DETECTION")
        await ctx.channel.send(f"@{ctx.author.name}, йой, козаче, кацапська заборонена в цьому чаті cmonBruh")


@bot.command(name='інфа')
async def show_info(ctx):
    await ctx.send(f"@{ctx.author.name}, мене звати ЩІЩ-Бот і я Ваш персональний помічник в чаті Піксельного. Наявні команди: \"!гпт\", \"!тг\", \"!шанс\", \"!дн @нік\", \"!hi @нік\", \"!окса\", \"!єнот\", \"!щіщ\"! Якщо Ви маєте ідеї стосовно мого покращення, будь ласка напишіть їх через \"!додай\" і це обов'язково допоможе мені стати краще. Щоб використати ChatGPT, просто тегніть @wuyodo і Ви отримаєте відповідь на питання GlitchCat")


@bot.command(name='тг')
async def telegram_show(ctx):
    await ctx.send(f"@{ctx.author.name}, аби не пропускати стріми Піксельного, підписуйтесь на наш Телеграм канал за посиланням @pixelfedya в пошуку Телеграму TehePelo")


@bot.command(name='єнот')
async def give_raccoon(ctx):
    username = ctx.content[5:]
    if "@" not in username:
        username = '@' + ctx.author.name
    await ctx.send(f"{username}, на єнота RaccAttack")


@bot.command(name='гпт')
async def gpt_instruction(ctx):
    await ctx.send(f"@{ctx.author.name}, для того, щоб отримати відповідь від ChatGPT, просто почніть Ваше повідомлення з @wuyodo і продовжіть Вашим питанням. Через деякий час ви отримаєте відповідь, згенеровану ботом ChatGPT :)")


@bot.command(name='щіщ')
async def say_sheesh(ctx):
    await ctx.send(f"ЩІІІІЩ")


@bot.command(name='окса')
async def say_hi_to_oxa(ctx):
    await ctx.send(f"Оксано, привіт!")


@bot.command(name='додай')
async def add_feature(ctx):
    await ctx.send(f"@seesmof, {ctx.content[6:]}, бігом додавати!")


@bot.command(name='hi')
async def telegram_show(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        username = '@' + ctx.author.name
    greetings = ["Здоров!", "Привіт!", "Вітаю!",
                 "Вітання!", "Як ся маєш?", "Слава Україні!", "Як воно?", "Бажаю здоров'я!", "Радий вітати!", "Радий бачити!", "Як справи?", "Як здоров'я?"]
    await ctx.send(f"{username}, {random.choice(greetings)}")


@bot.command(name='дн')
async def birthday_congrats(ctx):
    username = ctx.content[3:]
    # Congratulate the user
    greetings = ['З днем народження! Сьогодні день, коли здійснюються Ваші мрії і виконуються Ваші бажання. У цей особливий день я бажаю Вам щастя та успіху на все життя. Нехай благополуччя, радість і любов оточують Вас сьогодні і завжди. Всього найкращого в цей особливий день!', 'З Днем народження! Це Ваш особливий день, і я бажаю Вам щасливого святкування! Нехай цей день буде наповнений радістю, міцним здоров`ям і великою удачею. Нехай наступний рік буде сповнений успіхом та щастям. Насолоджуйтесь особливими моментами свого дня народження та цінуйте любов і тепло своїх близьких. Нехай наступний рік буде найкращим!',
                 'З Днем народження! Нехай цей особливий день буде наповнений радістю і сміхом. Нехай Ваше серце буде переповнене щастям, а дні будуть сповнені чудовими моментами. Бажаємо удачі та успіхів у всіх Ваших починаннях. Фантастичного дня!!', 'З Днем народження! Нехай цей особливий день буде наповнений радістю та світлими почуттями. Бажаємо Вам всього найкращого в житті, нехай здійсняться всі Ваші мрії та прагнення. Нехай наступний рік буде надзвичайно успішним!', 'Вітаємо з днем народження у цей особливий день! Нехай цей рік принесе Вам багато позитиву, радості та успіху. Бажаю Вам всього найкращого в житті, і нехай всі Ваші мрії здійсняться. Гарного дня та чудового наступного року!', 'Вітаємо з днем народження! Нехай цей особливий день буде наповнений морем веселощів, любові та сміху. Бажаю, щоб цей рік був чудовим і щоб Ви досягли всіх своїх цілей. Бажаю прекрасного життя, сповненого благословень. З днем народження!']
    await ctx.send(f'{username}, {random.choice(greetings)}')


@bot.command(name='шанс')
async def give_chance(ctx):
    chance = random.randint(1, 100)
    await ctx.send(f"@{ctx.author.name}, вірогідність цього становить {chance}%.")


if __name__ == "__main__":
    # launch bot
    bot.run()
