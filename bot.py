# include necessary libraries/files
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
from playsound import playsound

# for handling sound file location
sound_path = "D:\GitHub\python-twitchio-chat-bot\sound.mp3"
# for handling OpenAI API key
openai.api_key = "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"
# Then, you can call the "gpt-3.5-turbo" model
model_engine = "gpt-3.5-turbo"


def generate_response(input_text):
    # Send an API request and get a response, note that the interface and parameters have changed compared to the old model
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[{"role": "system", "content": "Ти - бот в чаті Твіч стрімера, якого звати Федя, він же Василь, Піксельний Федя або Піксельний. Твоя задача - допомагати користувачам чату. Ти спілкуєшся лише Українською та Англійською мовами. Якщо користувач звертається до тебе російською, реагуй виключно негативно і відмовляйся спілкуватись з ним."}, {
            "role": "user", "content": input_text}],
        max_tokens=150,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

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
        input_text = ctx.content[len("@wuyodo"):].strip()
        output_text = generate_response(input_text)
        try:
            await ctx.channel.send("@" + ctx.author.name + ", " + output_text)
        except Exception as e:
            await ctx.channel.send("@" + ctx.author.name + ", Ой-ой... Моє повідомлення не вмістилось в чат. Спробуйте трохи пізніши або змініть свій запит")

    names = ["seesmof", "сісмуф", "сісмоф", "seesmoff", "олег"]
    if check_for_letters(ctx.content.lower(), names):
        playsound(sound_path)

    letters = ["э", "ы", "ё", "ъ"]
    if check_for_letters(ctx.content.lower(), letters):
        await ctx.channel.send(f"@{ctx.author.name}, йой, козаче, міняй розкладку бо зара бан отримаєш cmonBruh")

    # relay message to command callbacks
    await bot.handle_commands(ctx)

    print(f"\n{ctx.author.name}: {ctx.content}")


@bot.command(name='інфа')
async def show_info(ctx):
    await ctx.send(f"@{ctx.author.name}, мене звати ЩІЩ-Бот і я Ваш персональний помічник в чаті Піксельного. Наявні команди: \"!гпт\", \"!тг\", \"!шанс\", \"!пр\", \"!окса\", \"!єнот\", \"!щіщ\", \"!гам\", \"!дн @нік\"! Якщо Ви маєте ідеї стосовно мого покращення, будь ласка напишіть їх через \"!додай\" і це обов'язково допоможе мені стати краще")


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


@bot.command(name='окса')
async def say_hi_to_oxa(ctx):
    await ctx.send(f"Оксано, привіт!")


@bot.command(name='додай')
async def add_feature(ctx):
    await ctx.send(f"@seesmof, {ctx.content[6:]}, бігом додавати!")


@bot.command(name='пр')
async def telegram_show(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        username = '@' + ctx.author.name
    greetings = ["Здоров!", "Привіт!", "Вітаю!",
                 "Вітання!", "Як ся маєш?", "Слава Україні!", "Як воно?", "Бажаю здоров'я!", "Радий вітати!", "Радий бачити!", "Як справи?", "Як здоров'я?"]
    await ctx.send(f"{username}, {random.choice(greetings)}")


@bot.command(name='hi')
async def telegram_show(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        username = '@' + ctx.author.name
    greetings = ["Hey!", "What's up?", "Yo!", "Greetings!", "Hi there!", "Howdy!", "How's it going?", "What's new?",
                 "Good day!", "What's happening?", "Sup?", "How's everything?", "What's up, buddy?", "Good to see you!"]
    await ctx.send(f"{username}, {random.choice(greetings)}")


@bot.command(name='гам')
async def telegram_show(ctx):
    username = ctx.content[4:]
    if "@" not in username:
        username = '@' + ctx.author.name
    shenanigans = ["Гамно", "гамно", "ГАМНО", "ГАМНООО",
                   "ГАМНОО", "ГАМНОООО", "Лайно", "лайно", "ЛАЙНО", "ЛАЙНОО", "ЛАЙНООО", "ЛАЙНОООО", "Гівно", "гівно", "ГІВНО", "ГІВНОО", "ГІВНООО", "ГІВНОООО"]
    await ctx.send(f"{username}, {random.choice(shenanigans)}")


@bot.command(name='щіщ')
async def telegram_show(ctx):
    username = ctx.content[4:]
    if "@" not in username:
        username = '@' + ctx.author.name
    shenanigans = ["щіщ", "ЩІЩ", "ЩІІЩ", "ЩІІІЩ", "ЩІІІІЩ"]
    await ctx.send(f"{username}, {random.choice(shenanigans)}")


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
