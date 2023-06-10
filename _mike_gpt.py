from twitchio.ext import commands
from vars import *
from mfs import *
import asyncio


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=GPT_TOKEN,
                         prefix='!', initial_channels=['mike09steelers', 'seesmof', 'PixelFedya'])
        self.lock = asyncio.Lock()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        async with self.lock:
            letters = ["@piprly", "@wuyodo"]
            if check_for_letters(message.content.lower(), letters) and message.author.name != "piprly":
                output_text = generate_ai_message(
                    message.content, message.author.name)
                output_text = split_long_gpt(output_text)
                for substr in output_text:
                    await message.channel.send(f"{substr}, @{message.author.name}")
                    await asyncio.sleep(20)
            await asyncio.sleep(20)


bot = Bot()
bot.run()
