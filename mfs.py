from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re

log_dir = "D:/repos/python-twitchio-chat-bot/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
