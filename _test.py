from twitchio.ext import commands
from vars import *
from mfs import *
import random


async def main():
    random_numbers = []
    for i in range(0, 10):
        random_numbers.append(random.randint(0, 9))

    for number in random_numbers:
        print(number)
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
