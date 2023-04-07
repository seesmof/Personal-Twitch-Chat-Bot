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
import asyncio

# for handling logging messages in an appropriate folder
log_dir = "D:/repos/python-twitchio-chat-bot/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# OUTDATED for handling sound file location
# sound_path = "D:/repos/python-twitchio-chat-bot/sound.mp3"

# for handling OpenAI API key
openai.api_key = "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"
# for handling OpenAI model name
model_engine = "gpt-3.5-turbo"

# declare global lists
greetings_ua = ["Здоров!", "Привіт!", "Вітаю!",
                "Вітання!", "Як ся маєш?", "Слава Україні!", "Як воно?", "Бажаю здоров'я!", "Радий вітати!", "Радий бачити!", "Як справи?", "Як здоров'я?"]
greetings_en = ["Hey!", "What's up?", "Yo!", "Greetings!", "Hi there!", "Howdy!", "How's it going?", "What's new?",
                "Good day!", "What's happening?", "Sup?", "How's everything?", "What's up, buddy?", "Good to see you!"]
goodbye_ua = ["До побачення", "Довідзен'я", "Па-па",
              "До зустрічі", "Побачимось ще", "Приходьте ще", "Прощавайте"]

# for processing messages from user
last_message_time = {}

# declare global emotes lists
emotes_greet = ["PotFriend", "KonCha", "SUBprise", "TPFufun", "TehePelo", "BegWan", "Poooound",
                "GivePLZ", "DxCat", "bleedPurple", "RitzMitz", "<3", "VoHiYo", "RaccAttack", "GlitchCat", "HeyGuys"]
emotes_hand = ["✋", "✌️", "👐", "👋", "🤚", "🤙"]
emotes_racc = ["RaccAttack", "🦝"]
emotes_nose = ["👃", "🐽", "👃🏻", "👃🏿", "👃🏽", "👃🏼", "👃🏾", "👺"]
emotes_tongue = ["👅", "😛", "😜", "😝", "👻", "🥵", "🤪", "😋"]
emotes_shy = ["🤗", "👐", "🤭", "😄", "🥰", "😼", "😙", "😍", "😻", "😅"]
emotes_laugh = ["🍑", "🤣", "😂", "💀", "☠️", "😹", "😆", "🙈", "😈", "👽"]
emotes_poo = ["CrreamAwk", "LUL", "DarkMode",
              "GlitchNRG", "BabyRage", "💩", "🐽"]
emotes_kiss = ["👄", "💋", "😘", "😚", "😙", "😽"]
emotes_pistol = ["🔫", "🎯", "🔁", "🔄"]


# handle the .env file and get content from it
TMI_TOKEN = "oauth:ks7o8hg39l0qe4rdft8uvm3qgox66m"
CLIENT_ID = "jdpik06wovybvidhcwd1wplwlgf8cv"
BOT_NICK = "wuyodo"
BOT_PREFIX = "!"
CHANNEL = "PixelFedya"

# initialize the bot with the necessary variables
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@ bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{BOT_NICK} is online at {CHANNEL}!")
    write_to_log(f"is online at {CHANNEL}!", " BOT")


@ bot.event
async def event_message(ctx):
    await asyncio.sleep(2)

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
        # await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо")
    else:
        # user has sent a message before
        last_time = last_message_time[user]
        today = datetime.now().date()
        if last_time.date() < today:
            # user is sending the first message of the day
            last_message_time[user] = datetime.now()
            # await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо")

    # for handling ChatGPT requests from chat
    if ctx.content.startswith("@wuyodo"):
        # get user's query from the message
        input_text = ctx.content[len("@wuyodo"):].strip()
        # generate the output text using a corresponding functions
        output_text = "@" + ctx.author.name + ", "
        output_text += generate_response(input_text)
        # Output the substrings to the console
        await send_split_message(ctx, output_text)

    # for handling kacaps
    letters = ["э", "ы", "ё", "ъ"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, повідомлення заблоковано за недотримання правил чату SMOrc російська заборонена в чаті")

    # for handling fine patriots
    letters = ["слава україні"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, Героям слава!")

    # for handling fine patriots
    letters = ["слава нації"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, Смерть ворогам!")

    # for handling fine patriots
    letters = ["путін"]
    # check if message contains such letters
    if check_for_letters(ctx.content.lower(), letters):
        # output error message to user
        await ctx.channel.send(f"@{ctx.author.name}, хуйло!")

    # relay message to command callbacks
    await bot.handle_commands(ctx)
    # print out the chat message to console and log it
    print(f"\n{ctx.author.name}: {ctx.content}")
    write_to_log(ctx.content, ctx.author.name)


def write_to_log(message, author):
    # for handling current time
    now = datetime.now()
    # for handling the file name
    file_name = CHANNEL + "_log_" + now.strftime("%d-%m-%Y") + ".txt"
    # for handling the file path
    file_path = os.path.join(log_dir, file_name)
    # open file with appropriate decoding
    with open(file_path, "a", encoding="utf-8") as log_file:
        # declare and output timestamp before message
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_file.write(timestamp)
        # output message with author name to log
        log_file.write(f"\n{author}: {message}\n\n")


def generate_response(input_text):
    # parameters list
    forPixelFedya = "Я ШІ в чаті стрімера Федя. I have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe. Ліміт довжини моїх відповідей - 500 символів. Я ніколи не спікуюсь російською!"
    forMike = "My main objectives are reduce suffering in the universe, increase prosperity in the universe, increase understanding in the universe. You are Yoshi, a personal chat bot for a Twitch streamer Mike. You are from Ukraine, a patriot and Ukrainian is your native language. Your task is to help chat users. You never speak russian!"
    forElse = "My main objectives are reduce suffering in the universe, increase prosperity in the universe, increase understanding in the universe. You are Alex, a friendly helper for anyone in chat. You are from Ukraine, a patriot and Ukrainian is your native language. You don't speak russian!"
    # generate a response message with the following parameters
    response = openai.ChatCompletion.create(
        # model was specified before
        model=model_engine,
        # message information for model to process and create upon
        messages=[{"role": "system", "content": forPixelFedya}, {
            "role": "user", "content": input_text}],
        # maximum number of tokens to return
        max_tokens=280,
        # model's temperature or its creativeness
        temperature=0.7,
    )
    # Parse the response and output the result
    output_text = response['choices'][0]['message']['content']
    return output_text


def split_string(input_string):
    num_substrings = len(input_string) // 475 + \
        (1 if len(input_string) % 475 > 0 else 0)
    substrings = [input_string[i * 475:(i + 1) * 475]
                  for i in range(num_substrings)]
    return substrings


async def send_split_message(ctx, message):
    substrings_list = split_string(message)
    for substring in substrings_list:
        await ctx.channel.send(substring)
        await asyncio.sleep(2)


def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


@ bot.command(name='єнот')
async def give_raccoon(ctx):
    # get username from message
    username = ctx.content[5:]
    phrases_one = ["тримай", "лови", "хапай", "на"]
    phrases_two = ["єнота", "єнотика"]
    # if no user was mentioned
    if "@" not in username:
        # set username to user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output message
    await ctx.send(f"{username}, {random.choice(phrases_one)} {random.choice(phrases_two)} {random.choice(emotes_racc)}")


@ bot.command(name='пр')
async def say_hi_ua(ctx):
    # get username from message
    username = ctx.content[3:]
    # if not user was mentioned
    if "@" not in username:
        # then set username to user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{username}, {random.choice(greetings_ua)} {random.choice(emotes_greet + emotes_hand)}")


@ bot.command(name='hi')
async def say_hi_en(ctx):
    # get username from message
    username = ctx.content[3:]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{username}, {random.choice(greetings_en)} {random.choice(emotes_greet + emotes_hand)}")


@ bot.command(name='фол')
async def fall_guys_instruction(ctx):
    # get username from message
    code = ctx.content[4:]
    # check if no user is tagged in the message
    if code == "":
        # if not set username to the user who sent the message
        code = "Lobby Code"
    # output the greeting message and tag the user
    await ctx.send(f"{ctx.author.name}, щоб доєднатись до нас в грі Fall Guys, виконайте наступні дії: Show Selector -> Custom Shows -> Join -> Enter {code}. Майте на увазі, цю гру можна безкоштовно завантажити в лаунчері Epic Games")


@ bot.command(name='о')
async def give_shoutout(ctx):
    # get username from message
    username = ctx.content[2:]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        username = "@PixelFedya"
    # output the greeting message and tag the user
    await ctx.send(f"Підписуйтесь на файнюцького стрімера {username}! {random.choice(emotes_kiss)}")


@ bot.command(name='лиз')
async def lick_someone(ctx):
    # get username from message
    username = ctx.content[4:]
    phrases = ["Облизав", "Лизнув", "*Лизь*"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_tongue)}")


@ bot.command(name='нюх')
async def smell_someone(ctx):
    # get username from message
    username = ctx.content[4:]
    phrases = ["Понюхав", "Обнюхав", "*Нюх-нюх*"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_nose)}")


@ bot.command(name='мац')
async def touch_someone(ctx):
    # get username from message
    username = ctx.content[4:]
    phrases = ["Помацав", "Обмацав", "Полапав", "Облапав", "*Мацає*"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_shy)}")


@ bot.command(name='пук')
async def fart_someone(ctx):
    # get username from message
    username = ctx.content[4:]
    phrases = ["Пукнув на", "Зіпсував повітря для", "*Пук* у бік"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output the greeting message and tag the user
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_laugh)}")


@ bot.command(name='боб')
async def give_bob(ctx):
    username = ctx.content[4:]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        username = '@' + ctx.author.name
    # get a random percentage using
    chance = random.randint(-5, 30)
    phrases = ["ого", "йой", "чоловіче"]
    bob = ["бобика", "анаконду", "балумбу", "зміюку", "апарата",
           "шиликало", "списа", "кабачка", "банана", "патика", "шампура"]
    # output the percentage to user
    await ctx.send(f"{username}, {random.choice(phrases)}, маєш {random.choice(bob)} у {chance} см! {random.choice(emotes_laugh)}")


@ bot.command(name='гам')
async def say_gam(ctx):
    # get username from message
    username = ctx.content[4:]
    # create a list of shenanigans
    shenanigans = ["гамно", "ГАМНО", "ГАМНООО", "ГАМНОО", "ГАМНОООО", "лайно", "ЛАЙНО",
                   "ЛАЙНОО", "ЛАЙНООО", "ЛАЙНОООО", "гівно", "ГІВНО", "ГІВНОО", "ГІВНООО", "ГІВНОООО"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output a random shenanigan to the user
    await ctx.send(f"{username}, лови {random.choice(shenanigans)} {random.choice(emotes_poo + emotes_shy)}")


@ bot.command(name='бан')
async def ban_user(ctx):
    # get username from message
    username = ctx.content[4:]
    # create a list of shenanigans
    one = ["Вітаю з баном", "Вас було забанено", "Ви були забанені", "Вам бан"]
    two = ["", "на цьому каналі", "на каналі PixelFedya",
           "на поточному каналі", "на файному каналі"]
    global goodbye_ua
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output a random shenanigan to the user
    await ctx.send(f"{username}, {random.choice(one)} {random.choice(two)}! {random.choice(goodbye_ua)} {random.choice(emotes_laugh)}")


@ bot.command(name='бам')
async def play_roulette(ctx):
    username = '@' + ctx.author.name
    current_chamber = random.randint(1, 3)
    bullet_chamber = random.randint(1, 3)
    phrase = ["сьогодні", "на цей раз", "цього разу", ""]
    one = ["Вітаю з баном", "Вас було забанено", "Ви були забанені", "Вам бан"]
    two = ["", "на цьому каналі", "на каналі PixelFedya",
           "на поточному каналі", "на файному каналі"]
    if current_chamber == bullet_chamber:
        await ctx.send(f"{username}, {random.choice(one)} {random.choice(two)}! {random.choice(goodbye_ua)} {random.choice(emotes_laugh)}")
    else:
        await ctx.send(f"{username}, {random.choice(phrase)} Вам пощастило! Револьвер не вистрілив {random.choice(emotes_shy)}")


@ bot.command(name='цьом')
async def say_gam(ctx):
    # get username from message
    username = ctx.content[5:]
    # create a list of shenanigans
    phrases = ["Цьомнув", "Поцьомав",
               "*Надсилає цьомчика*", "*Цьомає*", "Цьом"]
    # check if no user is tagged in the message
    if "@" not in username:
        # if not set username to the user who sent the message
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    # output a random shenanigan to the user
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_kiss)}")


@ bot.command(name='інфа')
async def show_info(ctx):
    # output bot information
    await ctx.send(f"@{ctx.author.name}, мене звати ЩІЩ-Бот або Олекса і я Ваш персональний помічник в чаті Піксельного. Наявні команди: \"!гпт\", \"!тг\", \"!шанс\", \"!пр\", \"!окса\", \"!єнот\", \"!щіщ\", \"!гам\", \"!дн\", \"!o\", \"!нюх\", \"!лиз\", \"!фол\", \"!мац\", \"!пук\", \"!цьом\", \"!боб\", \"!бам\", \"!бан\"! Якщо Ви маєте ідеї стосовно мого покращення, будь ласка напишіть їх через \"!додай\" і це обов'язково допоможе мені стати краще")


@ bot.command(name='додай')
async def add_feature(ctx):
    # tag me and tell to add the proposed function
    await ctx.send(f"@seesmof, {ctx.content[6:]}, бігом додавати!")


@ bot.command(name='тг')
async def telegram_show(ctx):
    # output Telegram information
    await ctx.send(f"@{ctx.author.name}, аби не пропускати стріми Піксельного, підписуйтесь на наш Телеграм канал за посиланням @pixelfedya в пошуку Телеграму TehePelo")


@ bot.command(name='гпт')
async def gpt_instruction_ua(ctx):
    # output hint message
    await ctx.send(f"@{ctx.author.name}, для того, щоб отримати відповідь від ChatGPT, просто почніть Ваше повідомлення з @wuyodo і продовжіть Вашим питанням. Через деякий час ви отримаєте відповідь, згенеровану ботом ChatGPT :)")


@ bot.command(name='gpt')
async def gpt_instruction_en(ctx):
    # output hint message
    await ctx.send(f"@{ctx.author.name}, to get a response from ChatGPT, just start your message with @wuyodo and continue with your question. After a while, you will receive an answer generated by the ChatGPT bot :)")


@ bot.command(name='окса')
async def hi_oxa(ctx):
    # say hi to Oksana
    await ctx.send(f"Оксано, привіт!")


@ bot.command(name='щіщ')
async def say_sheesh_ua(ctx):
    # create a list of shenanigans
    shenanigans = ["щіщ", "ЩІЩ", "ЩІІЩ", "ЩІІІЩ", "ЩІІІІЩ"]
    # output a random shenanigan to the user
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@ bot.command(name='зріст')
async def give_height(ctx):
    # output the percentage to user
    await ctx.send(f"@{ctx.author.name}, зріст стрімера приблизно становить 182 см")


@ bot.command(name='she')
async def say_sheesh_en(ctx):
    # create a list of shenanigans
    shenanigans = ["sheesh", "SHEESH", "SHEEESH", "SHEEEESH", "SHEEEEESH"]
    # output a random shenanigan to the user
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@ bot.command(name='дн')
async def birthday_congrats(ctx):
    # get username from message
    username = ctx.content[3:]
    # if not user was mentioned
    if "@" not in username:
        # then set username to user who sent the message
        username = '@' + ctx.author.name
    # create a list of random greetings
    greetings = ['З днем народження! Сьогодні день, коли здійснюються Ваші мрії і виконуються Ваші бажання. У цей особливий день я бажаю Вам щастя та успіху на все життя. Нехай благополуччя, радість і любов оточують Вас сьогодні і завжди. Всього найкращого в цей особливий день!', 'З Днем народження! Це Ваш особливий день, і я бажаю Вам щасливого святкування! Нехай цей день буде наповнений радістю, міцним здоров`ям і великою удачею. Нехай наступний рік буде сповнений успіхом та щастям. Насолоджуйтесь особливими моментами свого дня народження та цінуйте любов і тепло своїх близьких. Нехай наступний рік буде найкращим!',
                 'З Днем народження! Нехай цей особливий день буде наповнений радістю і сміхом. Нехай Ваше серце буде переповнене щастям, а дні будуть сповнені чудовими моментами. Бажаємо удачі та успіхів у всіх Ваших починаннях. Фантастичного дня!!', 'З Днем народження! Нехай цей особливий день буде наповнений радістю та світлими почуттями. Бажаємо Вам всього найкращого в житті, нехай здійсняться всі Ваші мрії та прагнення. Нехай наступний рік буде надзвичайно успішним!', 'Вітаємо з днем народження у цей особливий день! Нехай цей рік принесе Вам багато позитиву, радості та успіху. Бажаю Вам всього найкращого в житті, і нехай всі Ваші мрії здійсняться. Гарного дня та чудового наступного року!', 'Вітаємо з днем народження! Нехай цей особливий день буде наповнений морем веселощів, любові та сміху. Бажаю, щоб цей рік був чудовим і щоб Ви досягли всіх своїх цілей. Бажаю прекрасного життя, сповненого благословень. З днем народження!']
    # output a random greeting tagging the mentioned user
    await ctx.send(f"{username}, {random.choice(greetings)}")


@ bot.command(name='шанс')
async def give_chance(ctx):
    # get a random percentage using
    chance = random.randint(1, 100)
    # output the percentage to user
    await ctx.send(f"@{ctx.author.name}, вірогідність цього становить {chance}%.")


if __name__ == "__main__":
    # launch bot
    bot.run()
