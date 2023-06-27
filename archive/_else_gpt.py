from mfs import *
from vars import *

BOT_PREFIX = "!"
CHANNEL = "seesmof"


bot = commands.Bot(
    irc_token=GPT_TMI_TOKEN,
    client_id=GPT_CLIENT_ID,
    nick=GPT_BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@ bot.event
async def event_ready():
    print(f"{GPT_BOT_NICK} is online at {CHANNEL}!")
    write_to_log(f"is online at {CHANNEL}!", GPT_BOT_NICK, CHANNEL)


@ bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == GPT_BOT_NICK.lower():
        print(f"\nBOT: {ctx.content}")
        return

    letters = ["@wuyodo"]
    if check_for_letters(ctx.content.lower(), letters) and ctx.author.name.lower() != "pawrop":
        output_text = generate_ai_message(ctx.content, ctx.author.name)
        await send_split_gpt(ctx, output_text)
    await asyncio.sleep(20)


if __name__ == "__main__":
    bot.run()
