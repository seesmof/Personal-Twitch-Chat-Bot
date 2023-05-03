# include necessary libraries/files
from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands
from playsound import playsound
from datetime import datetime
import pygetwindow as gw

import openai
import random
import os
import asyncio
import pyautogui
import mfs
from vars import *

sound_path = "D:/repos/python-twitchio-chat-bot/sound.mp3"

last_message_time = {}
messages_tracker = {}

BOT_PREFIX = "!"
CHANNEL = "PixelFedya"
bot = commands.Bot(
    irc_token=STD_TMI_TOKEN,
    client_id=STD_CLIENT_ID,
    nick=STD_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@ bot.event
async def event_ready():
    # print bot and channel name when it activates
    print(f"{STD_BOT_NICK} is online at {CHANNEL}!")
    # log it
    mfs.write_to_log(f"is online at {CHANNEL}!", STD_BOT_NICK, CHANNEL)


@ bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == STD_BOT_NICK.lower():
        print(f"\nBOT: {ctx.content}")
        mfs.write_to_log(ctx.content, STD_BOT_NICK, CHANNEL)
        return
    elif ctx.author.name.lower() == "streamelements":
        print(f"\nBOT: {ctx.content}")
        return

    global last_message_time
    user = ctx.author.name
    if user not in last_message_time:
        last_message_time[user] = datetime.now()

        # OUTDATED greet the user with a random greeting
        # await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо")
    else:
        last_time = last_message_time[user]
        today = datetime.now().date()
        if last_time.date() < today:
            last_message_time[user] = datetime.now()

            # OUTDATED greet the user with a random greeting
            # await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо")

    if ctx.author.name not in messages_tracker:
        messages_tracker[ctx.author.name] = []
    messages_tracker[ctx.author.name].append(ctx.content)

    letters = ["@pawrop"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        phrases = ["нажаль, я не можу відповісти на ваше повідомлення",
                   "я не знаю відповіді на це", "я не здатний генерувати повідомлення"]
        await ctx.channel.send(f"@{ctx.author.name}, {random.choice(phrases)}. Краще спитайте wuyodo :) Введіть !гпт у чат, щоб дізнатися більше")

    letters = ["э", "ы", "ё", "ъ"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        await ctx.channel.send(f"@{ctx.author.name}, повідомлення заблоковано за недотримання правил чату SMOrc російська заборонена в чаті")

    letters = ["слава україні"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        await ctx.channel.send(f"@{ctx.author.name}, Героям слава!")

    letters = ["слава нації"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        await ctx.channel.send(f"@{ctx.author.name}, Смерть ворогам!")

    letters = ["путін"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        letterX = ["x", "х", "ẋ"]
        letterY = ["y", "у", "ẙ"]
        letterO = ["о", "o", "ø", "ǿ", "ö", "ȫ", "ó", "ò", "ô",
                   "ố", "ȱ", "ȯ", "ȏ", "ŏ", "ő", "ǒ", "ộ", "ỗ", "ổ", "ồ", "ọ", "ơ", "ỏ", "ở", "ợ", "ỡ", "ờ", "ớ", "ᴏ", "ᴑ"]
        await ctx.channel.send(f"@{ctx.author.name}, {random.choice(letterX)}{random.choice(letterY)}йл{random.choice(letterO)}!")

    letters = ["seesmof", "seesmoff", "сісмуф", "сісмоф"]
    if mfs.check_for_letters(ctx.content.lower(), letters):
        playsound(sound_path)

    ''' Temporarily disabled
    # for handling greetings
    letters = ["дороу", "привіт", "здороу", "здоров", "доров", "хай", "буено", "вітаю", "доброго вечора",
               "добрий вечір", "вітамба", "доброго дня", "добрий день", "доброго ранку", "добрий ранок", "вітання", "як ся маєш", "як воно", "бажаю здоров'я", "радий вітати", "радий бачити", "як справи", "як здоров'я", "hey", "hello", "hiya"]
    # check if message contains the greeting
    if mfs.check_for_letters(ctx.content.lower(), letters):
        # greet the user
        await ctx.channel.send(f"@{user}, {random.choice(greetings_ua)} Ласкаво просимо")
    '''

    await bot.handle_commands(ctx)
    print(f"\n{ctx.author.name}: {ctx.content}")
    mfs.write_to_log(ctx.content, ctx.author.name, CHANNEL)
    await asyncio.sleep(2)


@ bot.command(name='інфа', aliases=['info', 'інформація'])
async def show_info(ctx):
    await ctx.send(f"@{ctx.author.name}, мене звати ЩІЩ-Бот і я Ваш персональний ШІ-помічник в чаті Піксельного. Ви можете поставити мені будь-яке питання, просто додавши \"@wuyodo\" до свого повідомлення. Також, щоб подивитись мої існуючі команди, напишіть \"!коми\" в чат. Якщо Ви маєте ідеї стосовно мого покращення, будь ласка, напишіть їх через \"!додай\" і це обов'язково допоможе мені стати краще")


@ bot.command(name='коми', aliases=['help', 'команди'])
async def show_commands(ctx):
    await ctx.send(f"@{ctx.author.name}, Наявні команди: \"!єнот\", \"!пр\", \"!hi\", \"!фол\", \"!о\", \"!лиз\", \"!нюх\", \"!мац\", \"!пук\", \"!боб\", \"!гам\", \"!бан\", \"!бам\", \"!цьом\", \"!додай\", \"!тг\", \"!гпт\", \"!gpt\", \"!окса\", \"!щіщ\", \"!зріст\", \"!she\", \"!дн\", \"!шанс\", \"!ем\", \"!пк\", \"!мак\", \"!чого\", \"!де\", \"!блін\", \"!ой\", \"!батько\", \"!коц\", \"!шлик\", \"!дуп\"")


@ bot.command(name='єнот')
async def give_raccoon(ctx):
    username = ctx.content[5:]
    phrases_one = ["тримай", "лови", "хапай", "на"]
    phrases_two = ["єнота", "єнотика"]
    # if no user was mentioned
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{username}, {random.choice(phrases_one)} {random.choice(phrases_two)} {random.choice(emotes_racc)}")


@ bot.command(name='пр')
async def say_hi_ua(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{username}, {random.choice(greetings_ua)} {random.choice(emotes_greet + emotes_hand)}")


@ bot.command(name='hi')
async def say_hi_en(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{username}, {random.choice(greetings_en)} {random.choice(emotes_greet + emotes_hand)}")


@ bot.command(name='фол', aliases=['fall', 'fg'])
async def fall_guys_instruction(ctx):
    code = ctx.content[4:]
    if code == "":
        code = "Lobby Code"
    await ctx.send(f"@{ctx.author.name}, щоб доєднатись до нас в грі Fall Guys, виконайте наступні дії: Show Selector -> Custom Shows -> Join -> Enter {code}. Майте на увазі, цю гру можна безкоштовно завантажити в лаунчері Epic Games і важить вона 5,42ГБ")


@ bot.command(name='о', aliases=['so', 'шатаут'])
async def give_shoutout(ctx):
    username = ctx.content[2:]
    if "@" not in username:
        username = "@PixelFedya"
    await ctx.send(f"Підписуйтесь на файнюцького стрімера {username}! {random.choice(emotes_kiss)}")


@ bot.command(name='лиз')
async def lick_someone(ctx):
    username = ctx.content[4:]
    phrases = ["Облизав", "Лизнув", "*Лизь*"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_tongue)}")


@ bot.command(name='нюх')
async def smell_someone(ctx):
    username = ctx.content[4:]
    phrases = ["Понюхав", "Обнюхав", "*Нюх-нюх*"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_nose)}")


@ bot.command(name='мац')
async def touch_someone(ctx):
    username = ctx.content[4:]
    phrases = ["Помацав", "Обмацав", "Полапав", "Облапав", "*Мацає*"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_shy)}")


@ bot.command(name='пук')
async def fart_someone(ctx):
    username = ctx.content[4:]
    phrases = ["Пукнув на", "Зіпсував повітря для", "*Пук* у бік"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_laugh)}")


@ bot.command(name='боб', aliases=['бобик'])
async def give_bob(ctx):
    username = ctx.content[4:]
    if "@" not in username:
        username = '@' + ctx.author.name
    chance = random.randint(-5, 30)
    phrases = ["ого", "йой", "чоловіче"]
    bob = ["бобика", "анаконду", "балумбу", "зміюку", "апарата",
           "шиликало", "списа", "кабачка", "банана", "патика", "шампура"]
    await ctx.send(f"{username}, {random.choice(phrases)}, маєш {random.choice(bob)} у {chance} см! {random.choice(emotes_laugh)}")


@ bot.command(name='гам')
async def say_gam(ctx):
    username = ctx.content[4:]
    shenanigans = ["гамно", "ГАМНО", "ГАМНООО", "ГАМНОО", "ГАМНОООО", "лайно", "ЛАЙНО",
                   "ЛАЙНОО", "ЛАЙНООО", "ЛАЙНОООО", "гівно", "ГІВНО", "ГІВНОО", "ГІВНООО", "ГІВНОООО"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{username}, лови {random.choice(shenanigans)} {random.choice(emotes_poo + emotes_shy)}")


@ bot.command(name='бан')
async def ban_user(ctx):
    username = ctx.content[4:]
    one = ["Вітаю з баном", "Вас було забанено", "Ви були забанені", "Вам бан"]
    two = ["", "на цьому каналі", "на каналі PixelFedya",
           "на поточному каналі", "на файному каналі"]
    global goodbye_ua
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
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
    roll = ["Розкручую", "Кручу", "Прокручую"]
    if current_chamber == bullet_chamber:
        await ctx.send(f"{random.choice(roll)} барабан... {random.choice(emotes_pistol)} {username}, {random.choice(one)} {random.choice(two)}! {random.choice(goodbye_ua)} {random.choice(emotes_laugh)}")
    else:
        await ctx.send(f"{random.choice(roll)} барабан... {random.choice(emotes_pistol)} {username}, {random.choice(phrase)} Вам пощастило! Револьвер не вистрілив {random.choice(emotes_shy)}")


@ bot.command(name='цьом')
async def say_gam(ctx):
    username = ctx.content[5:]
    phrases = ["Цьомнув", "Поцьомав",
               "*Надсилає цьомчика*", "*Цьомає*", "Цьом"]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"{random.choice(phrases)} {username} {random.choice(emotes_kiss)}")


@ bot.command(name='додай')
async def add_feature(ctx):
    await ctx.send(f"@seesmof, {ctx.content[6:]}, бігом додавати!")


@ bot.command(name='тг')
async def telegram_show(ctx):
    await ctx.send(f"@{ctx.author.name}, аби не пропускати стріми Піксельного, підписуйтесь на наш Телеграм канал за посиланням @pixelfedya в пошуку Телеграму TehePelo")


@ bot.command(name='гпт')
async def gpt_instruction_ua(ctx):
    await ctx.send(f"@{ctx.author.name}, для того, щоб отримати відповідь від ChatGPT, просто почніть Ваше повідомлення з @wuyodo і продовжіть Вашим питанням. Через деякий час ви отримаєте відповідь, згенеровану ботом ChatGPT :)")


@ bot.command(name='gpt')
async def gpt_instruction_en(ctx):
    await ctx.send(f"@{ctx.author.name}, to get a response from ChatGPT, just start your message with @wuyodo and continue with your question. After a while, you will receive an answer generated by the ChatGPT bot :)")


@ bot.command(name='окса')
async def hi_oxa(ctx):
    await ctx.send(f"Оксано, привіт!")


@ bot.command(name='щіщ', aliases=['шіш', 'щіш', 'шіщ'])
async def say_sheesh_ua(ctx):
    shenanigans = ["щіщ", "ЩІЩ", "ЩІІЩ", "ЩІІІЩ", "ЩІІІІЩ"]
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@ bot.command(name='зріст')
async def give_height(ctx):
    await ctx.send(f"@{ctx.author.name}, зріст стрімера приблизно становить 182 см")


@ bot.command(name='she')
async def say_sheesh_en(ctx):
    shenanigans = ["sheesh", "SHEESH", "SHEEESH", "SHEEEESH", "SHEEEEESH"]
    await ctx.send(f"@{ctx.author.name}, {random.choice(shenanigans)}")


@ bot.command(name='дн')
async def birthday_congrats(ctx):
    username = ctx.content[3:]
    if "@" not in username:
        username = '@' + ctx.author.name
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


@ bot.command(name='ем', aliases=['емоджі', 'емоція', 'emoji', 'em'])
async def print_random_emoji(ctx):
    global_emotes_list = emotes_all_twitch
    # output a random shenanigan to the user
    await ctx.send(random.choice(global_emotes_list))


@ bot.command(name='пк')
async def show_pc_specs(ctx):
    # output a random shenanigan to the user
    await ctx.send(f"@{ctx.author.name}, процесор - i7-13700K, відеокарта - Geforce RTX 3080, камера - Logitech BRIO 4K, пам'ять - 32 ГБ")


@ bot.command(name='мак', aliases=['слимак', 'слимачок'])
async def act_slug(ctx):
    phrases = ["Можливо, я повільний, але я завжди у русі. Ніколи не знаєш, де я можу опинитися наступного разу!",
               "Я справжній поштовий равлик. Тільки не сподівайтеся, що я доставлю щось вчасно",
               "Нехай у мене немає мушлі, але мені все одно заздрять усі равлики",
               "Я нікуди не поспішаю, я просто насолоджуюся подорожжю. Навіть якщо це займе у мене цілий день",
               "Може, я й маленький, але я дуже люблю залишати сліди",
               "Я не лінивий, я просто зберігаю свою енергію на той час, коли вона мені дійсно потрібна",
               "Я не заблукав, я просто йду мальовничим маршрутом",
               "Можливо, я не найшвидший, але я точно найспритніший",
               "Я не слизький, я просто випромінюю свою природну чарівність,"
               "Я не слимак, я слимак-зайчик!"
               "Я не равлик, я переодягнений слимак. Тсс, нікому не кажи",
               "Можливо, у мене немає хребта, але я можу постояти за себе",
               "Я не повільний, я просто насолоджуюся моментом",
               "Я не слимак, я слимацька суперзірка!",
               "Мій панцир не просто для показухи, це мій пересувний дім",
               "Я не просто равлик, я ніндзя уповільненої дії",
               "Я не люблю дощ, це все одно, що приймати душ в одязі",
               "Я равлик, а не черепаха. Зрозумійте це правильно, люди!",
               "Я не лінивий, я просто економлю енергію",
               "Я не шкідник саду, я його прикрашаю",
               "Я не просто равлик, я швидкісний гонщик в сповільненій зйомці",
               "Я не боюся птахів, вони мене просто підвозять",
               "Я не закуска, я делікатес",
               "Я не слизький, я просто трохи вологий",
               "Я не повільний, я просто не поспішаю",
               "Я не слимак, я равлик зі стилем",
               "Я не повільний, я просто насолоджуюся життям",
               "Може, я і слизький, але принаймні не липкий",
               "Я, можливо, маленький, але у мене велика особистість",
               "Я не боюся птахів, це птахи бояться мене",
               "Я не шкідник, я гість",
               "Я не слизький, я спритний",
               "Я не просто слимак, я замаскований супергерой",
               "Я як равлик, але без будиночка",
               "Я не нудний, мене просто не розуміють",
               "Можливо, я повільний, але в кінці кінців я завжди досягаю мети",
               "Тихіше їдеш - далі будеш, друже!"
               "Не дозволяй нікому казати тобі, що ти не можеш чогось досягти, навіть якщо це займе певний час",
               "Ти можеш бути маленьким, але по-своєму сильним!",
               "Продовжуй рухатися вперед, навіть якщо це лише потроху за раз",
               "Кожна подорож починається з одного кроку, або, як у моєму випадку, з одного слизького сліду",
               "Вір у себе, навіть коли інші не вірять",
               "Не поспішай, і ти все одно досягнеш мети",
               "Шлях до успіху може бути довгим, але врешті-решт він того вартий",
               "Ніколи не здавайся, навіть коли стає важко",
               "Життя сповнене перешкод, але у тебе є сили, щоб їх подолати",
               "Ти не повільний, ти просто насолоджуєшся подорожжю",
               "Не порівнюй себе з іншими, ти по-своєму унікальний",
               "Найголовніше - це продовжувати рухатися вперед, незалежно від того, наскільки малим є прогрес",
               "Пам'ятай, що кожна невдача - це лише підготовка до майбутнього успіху",
               "Ти не просто слимак, ти першопроходець!",
               "Не дозволяй нікому притупити твою іскру, продовжуй сяяти!",
               "Подорож може бути довгою, але вид з вершини того вартий",
               "У тебе всередині є сила, щоб досягти всього, що ти захочеш",
               "Навіть равлики колись були слимаками, тому продовжуй рухатися вперед і ти досягнеш мети"
               ]
    await ctx.send(f"@{ctx.author.name}, {random.choice(phrases)} {random.choice(emotes_slug)}")


@ bot.command(name='чого')
async def who_is_he(ctx):
    await ctx.send(f"@{ctx.author.name}, стрімера звати Василь, але він має прізвище Фединяк, тому друзі називають його Федя. Ви можете називати його як вам завгодно :)")


@ bot.command(name='де')
async def where_from(ctx):
    await ctx.send(f"@{ctx.author.name}, стрімер родом з Івано-Франківської області, але наразі перебуває в Англії :)")


@ bot.command(name='блін')
async def no_ignore_please(ctx):
    await ctx.send(f"@PixelFedya")
    await asyncio.sleep(2)
    input_txt = ctx.content[5:]
    await mfs.send_split_gpt(ctx, input_txt)
    await asyncio.sleep(2)
    await ctx.send(f"@PixelFedya")


def replace_characters(string, char_dict):
    new_string = ""
    for char in string:
        if char in char_dict:
            new_string += char_dict[char]
        else:
            new_string += char
    return new_string


@ bot.command(name='ой', aliases=['дідько', 'бля'])
async def oh_no_my_keyboard(ctx):
    message = messages_tracker[ctx.author.name][-2]
    output_text = replace_characters(message, letters_dict)
    await ctx.send(f"@{ctx.author.name}, {output_text}")


@ bot.command(name='батько', aliases=['бат', 'батя'])
async def who_father(ctx):
    username = '@' + random.choice(list(last_message_time))
    phrase = ["мабуть є", "то є", "скоріш за все є",
              "походу є", "то, нажаль, є"]
    await ctx.send(f"@{ctx.author.name}, твій батько {random.choice(phrase)} {username} {random.choice(emotes_all_twitch)}")


@ bot.command(name='шлик', aliases=['члик', 'сюди'])
async def invoke_duel(ctx):
    username = ctx.content[5:]
    if "@" not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    phrase = ["шиликнув", "пошиликав", "чиликнув", "почиликав"]
    phrase_two = ["яйоли", "яєчки", "яйки", "balls", "cock", "бобика", "анаконду", "балумбу", "зміюку", "апарата",
                  "шиликало", "списа", "кабачка", "банана", "патика", "шампура"]
    await ctx.send(f"@{ctx.author.name}, {random.choice(phrase)} за {random.choice(phrase_two)} {username}  {random.choice(emotes_all_twitch)}")


@ bot.command(name='коц', aliases=['буц', 'яйк'])
async def easter_fight(ctx):
    username = ctx.content[4:]
    if '@' not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    users = [ctx.author.name, username]
    result = random.choice(users)
    await ctx.send(f"@{ctx.author.name}, цокнувся яйолами з {username}. {result} переміг!")


@ bot.command(name='дуп', aliases=['поп', 'ass'])
async def easter_fight(ctx):
    phrases = ["показав", "помацав", "полапав", "пощупав"]
    wut = ["дупу", "сраку"]
    username = ctx.content[4:]
    if '@' not in username:
        global last_message_time
        username = '@' + random.choice(list(last_message_time))
    await ctx.send(f"@{ctx.author.name} {random.choice(phrases)} {random.choice(wut)} {username} {random.choice(emotes_all_twitch)}")

if __name__ == "__main__":
    bot.run()
