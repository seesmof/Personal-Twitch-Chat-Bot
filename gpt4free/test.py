from gpt4free import usesless
from library import *

output_text = ""
output_text = generate_ai_message(
        message.content, message.author.name)
output_text = split_long_gpt(output_text)
for substr in output_text:
    await message.channel.send(f"{substr} @{message.author.name}")
    await asyncio.sleep(20)