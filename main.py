from twitchio.ext import commands
from mfs import *


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN,
                         prefix='!', initial_channels=WANTED_CHANNELS)
        self.lock = asyncio.Lock()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        try:
            async with self.lock:
                if message.author.name == BOT_NICK:
                    return
                letters = [f"@{BOT_NICK}"]
                output_text = ""

                if check_for_letters(message.content.lower(), letters):
                    output_text = AI(message.content)

                    print(
                        f"\nPROMPT: {message.content} by {message.author.name} at {message.channel.name}\n\nRESPONSE: {output_text}\n")
                    if LOGGING:
                        write_to_log(message.content, message.author.name,
                                     message.channel.name, output_text)

                    split_text = split_long_gpt(output_text)
                    for substr in split_text:
                        await message.channel.send(f"{substr} @{message.author.name}")
                        await asyncio.sleep(DELAY)
        except Exception as e:
            pass


bot = Bot()
bot.run()
