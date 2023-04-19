from twitchio.ext import commands
from datetime import datetime
import openai
import os
import asyncio
import time
import requests
import re
import mfs
from vars import *


async def check_streamer_status():
    # Create a Twitch client instance
    client = twitchio.Client(
        client_id=client_id, nick=bot_name, initial_channels=[streamer_name])

    # Connect to Twitch
    await client.connect()

    # Retrieve the streamer object
    streamer = await client.get_users(streamer_name)

    if streamer and streamer[0].is_live:
        # If the streamer is live, print a message saying so
        print(f"{streamer_name} is currently live!")
    else:
        # If the streamer is not live, print a message saying so
        print(f"{streamer_name} is currently offline.")

    # Disconnect from Twitch
    await client.disconnect()

# Run the async function to check the streamer status
asyncio.run(check_streamer_status())
