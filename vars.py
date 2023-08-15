
import os

TOKEN = "m56jxhrfo0hdjuieersxj9gk1gjsvl"
BOT_NICK = "piprly"
DELAY = 3.0
WANTED_CHANNELS = ["PixelFedya", "seesmof"]
BLOCKED_USERS = [""]
ALLOW_MEMORY = True
LOGGING = True
PERSONA = ""

if LOGGING:
    log_dir = "./logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
