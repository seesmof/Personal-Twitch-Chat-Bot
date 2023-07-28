from archive.mfs import *
from archive.vars import *

BOT_PREFIX = "!"
CHANNEL = "k3ned1"
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
        write_to_log(ctx.content, GPT_BOT_NICK, CHANNEL)
        return

    letters = ["@wuyodo"]
    if check_for_letters(ctx.content.lower(), letters) and ctx.author.name.lower() == "k3ned1":
        output_text = generate_ai_message(ctx.content, ctx.author.name)
        await send_split_gpt(ctx, output_text)
    await asyncio.sleep(1)


if __name__ == "__main__":
    bot.run()
