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
CHANNEL = "seesmof"

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
greetings_ua = ["Здоров!", "Привіт!", "Вітаю!",
                "Вітання!", "Як ся маєш?", "Слава Україні!", "Як воно?", "Бажаю здоров'я!", "Радий вітати!", "Радий бачити!", "Як справи?", "Як здоров'я?"]
# create a list of greetings
greetings_en = ["Hey!", "What's up?", "Yo!", "Greetings!", "Hi there!", "Howdy!", "How's it going?", "What's new?",
                "Good day!", "What's happening?", "Sup?", "How's everything?", "What's up, buddy?", "Good to see you!"]
last_message_time = {}


@bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{BOT_NICK} is online at {CHANNEL}!")


@bot.event
async def event_message(ctx):
    # the bot should not react to itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        # print out bot's message to log
        print(f"\nBOT: {ctx.content}")
        return

    global last_message_time
    user = ctx.author.name
    if user not in last_message_time:
        # user is sending the first message of the day
        last_message_time[user] = datetime.now()
        await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо KonCha")
    else:
        # user has sent a message before
        last_time = last_message_time[user]
        today = datetime.now().date()
        if last_time.date() < today:
            # user is sending the first message of the day
            last_message_time[user] = datetime.now()
            await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо KonCha")

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
            await ctx.channel.send("@" + ctx.author.name + ", Ой-ой... Моє повідомлення не вмістилось в чат. Спробуйте трохи пізніши або змініть свій запит")

    # for handling pings for myself
    names = ["seesmof", "сісмуф", "сісмоф", "seesmoff", "олег"]
    # check if message contains my name and play a ping sound if so
    if check_for_letters(ctx.content.lower(), names):
        playsound(sound_path)

    # for handling kacaps
    letters = ["э", "ы", "ё", "ъ"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, йой, козаче, міняй розкладку бо зара бан отримаєш cmonBruh")

    # relay message to command callbacks
    await bot.handle_commands(ctx)

    # print out the chat message to console and log it
    print(f"\n{ctx.author.name}: {ctx.content}")


async def generate_response(input_text):
    # generate a response message with the following parameters
    response = openai.ChatCompletion.create(
        # model was specified before
        model=model_engine,
        # message information for model to process and create upon
        messages=[{"role": "system", "content": "Ти - Олекса, бот в чаті Твіч стрімера, якого звати Піксельний Федя. Твоя задача - допомагати користувачам чату. Ти не спілкуєшся російською."}, {
            "role": "user", "content": input_text}],
        # maximum number of tokens to return
        max_tokens=100,
        # model's temperature or its creativeness
        temperature=0.7,
    )
    if response.choices[0].text == "flagged":
        # Do something here if the message is flagged
        warning_message = "Ваше повідомлення було позначено як неприйнятне. Будь ласка, утримайтеся від використання образливих висловлювань у майбутньому."
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


@bot.command(name='інфа')
async def show_info(ctx):
    # output bot information
    await ctx.send(f"@{ctx.author.name}, мене звати ЩІЩ-Бот або Олекса і я Ваш персональний помічник в чаті Піксельного. Наявні команди: \"!гпт\", \"!тг\", \"!шанс\", \"!пр\", \"!окса\", \"!єнот\", \"!щіщ\", \"!гам\", \"!дн\"! Якщо Ви маєте ідеї стосовно мого покращення, будь ласка напишіть їх через \"!додай\" і це обов'язково допоможе мені стати краще")


@bot.command(name='тг')
async def telegram_show(ctx):
    # output Telegram information
    await ctx.send(f"@{ctx.author.name}, аби не пропускати стріми Піксельного, підписуйтесь на наш Телеграм канал за посиланням @pixelfedya в пошуку Телеграму TehePelo")


@bot.command(name='єнот')
async def give_raccoon(ctx):
    # get username from message
    username = ctx.content[5:]
    # if no user was mentioned
    if "@" not in username:
        # set username to user who sent the message
        username = '@' + ctx.author.name
    # output message
    await ctx.send(f"{username}, на єнота RaccAttack")


@bot.command(name='гпт')
async def gpt_instruction(ctx):
    # output hint message
    await ctx.send(f"@{ctx.author.name}, для того, щоб отримати відповідь від ChatGPT, просто почніть Ваше повідомлення з @wuyodo і продовжіть Вашим питанням. Через деякий час ви отримаєте відповідь, згенеровану ботом ChatGPT :)")


@bot.command(name='окса')
async def say_hi_to_oxa(ctx):
    # say hi to Oksana
    await ctx.send(f"Оксано, привіт!")


@bot.command(name='додай')
async def add_feature(ctx):
    # tag me and tell to add the proposed function
    await ctx.send(f"@seesmof, {ctx.content[6:]}, бігом додавати!")


@bot.command(name='пр')
async def say_hi_Ukrainian(ctx):
    # get username from message
    username = ctx.content[3:]
    # if not user was mentioned
    if "@" not in username:
        # then set username to user who sent the message
        username = '@' + ctx.author.name
    # output the greeting message and tag the user
    await ctx.send(f"{username}, {random.choice(greetings_ua)}")


@bot.command(name='hi')
async def say_hi_English(ctx):
    # get username from message
    username = ctx.content[3:]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        username = '@' + ctx.author.name
    # output the greeting message and tag the user
    await ctx.send(f"{username}, {random.choice(greetings_en)}")


@bot.command(name='гам')
async def telegram_show(ctx):
    # create a list of shenanigans
    shenanigans = ["Гамно", "гамно", "ГАМНО", "ГАМНООО",
                   "ГАМНОО", "ГАМНОООО", "Лайно", "лайно", "ЛАЙНО", "ЛАЙНОО", "ЛАЙНООО", "ЛАЙНОООО", "Гівно", "гівно", "ГІВНО", "ГІВНОО", "ГІВНООО", "ГІВНОООО"]
    # output a random shenanigan to the user
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@bot.command(name='щіщ')
async def telegram_show(ctx):
    # create a list of shenanigans
    shenanigans = ["щіщ", "ЩІЩ", "ЩІІЩ", "ЩІІІЩ", "ЩІІІІЩ"]
    # output a random shenanigan to the user
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@bot.command(name='дн')
async def birthday_congrats(ctx):
    # get username from the message
    username = ctx.content[3:]
    # create a list of random greetings
    greetings = ['З днем народження! Сьогодні день, коли здійснюються Ваші мрії і виконуються Ваші бажання. У цей особливий день я бажаю Вам щастя та успіху на все життя. Нехай благополуччя, радість і любов оточують Вас сьогодні і завжди. Всього найкращого в цей особливий день!', 'З Днем народження! Це Ваш особливий день, і я бажаю Вам щасливого святкування! Нехай цей день буде наповнений радістю, міцним здоров`ям і великою удачею. Нехай наступний рік буде сповнений успіхом та щастям. Насолоджуйтесь особливими моментами свого дня народження та цінуйте любов і тепло своїх близьких. Нехай наступний рік буде найкращим!',
                 'З Днем народження! Нехай цей особливий день буде наповнений радістю і сміхом. Нехай Ваше серце буде переповнене щастям, а дні будуть сповнені чудовими моментами. Бажаємо удачі та успіхів у всіх Ваших починаннях. Фантастичного дня!!', 'З Днем народження! Нехай цей особливий день буде наповнений радістю та світлими почуттями. Бажаємо Вам всього найкращого в житті, нехай здійсняться всі Ваші мрії та прагнення. Нехай наступний рік буде надзвичайно успішним!', 'Вітаємо з днем народження у цей особливий день! Нехай цей рік принесе Вам багато позитиву, радості та успіху. Бажаю Вам всього найкращого в житті, і нехай всі Ваші мрії здійсняться. Гарного дня та чудового наступного року!', 'Вітаємо з днем народження! Нехай цей особливий день буде наповнений морем веселощів, любові та сміху. Бажаю, щоб цей рік був чудовим і щоб Ви досягли всіх своїх цілей. Бажаю прекрасного життя, сповненого благословень. З днем народження!']
    # output a random greeting tagging the mentioned user
    await ctx.send(f"{username}, {random.choice(greetings)}")


@bot.command(name='шанс')
async def give_chance(ctx):
    # get a random percentage using
    chance = random.randint(1, 100)
    # output the percentage to user
    await ctx.send(f"@{ctx.author.name}, вірогідність цього становить {chance}%.")


if __name__ == "__main__":
    # launch bot
    bot.run()
