from twitchio.ext import commands
from mfs import *


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN,
                         prefix='!', initial_channels=WANTED_CHANNELS)
        self.lock = asyncio.Lock()

    async def command_mine_info(self, message):
        await message.channel.send(f"Якщо ви раптом померли на нашому гардкор сервері в Minecraft, ви можете використати нагороду за бали під назвою \"Майнкрафт\", поточна ціна - 10,000 балів, аби повернутися на сервер і продовжувати грати з нами. @{message.author.name}")

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo or message.author.name in BLOCKED_USERS:
            return

        try:
            async with self.lock:
                letters = [f"@{BOT_NICK}"]
                output_text = ""

                if check_for_letters(message.content.lower(), letters):
                    output_text = generate_ai_message(message.content)

                    print(
                        f"\nPROMPT: {message.content} by {message.author.name} at {message.channel.name}\n\nRESPONSE: {output_text}\n")
                    if LOGGING:
                        write_to_log(message.content, message.author.name,
                                     message.channel.name, output_text)

                    split_text = split_long_gpt(output_text)
                    for substr in split_text:
                        await message.channel.send(f"{substr} @{message.author.name}")
                        await asyncio.sleep(DELAY)

                # MINECRAFT
                letters = [f"!майн", f"!майнкрафт"]
                if check_for_letters(message.content.lower(), letters):
                    await self.command_mine_info(message)
        except Exception as e:
            pass


bot = Bot()
bot.run()
