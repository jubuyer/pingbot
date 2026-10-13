# Bot that scans channels and pings users if new message id is detected
import discord
import asyncio
import os
import time
from dotenv import load_dotenv

# load env vars
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

USER_1 = int(os.getenv("USER_1"))
USER_2 = int(os.getenv("USER_2"))
# comma-separated channel ids the bot is allowed to ping in
CHANNEL_IDS = {int(c) for c in os.getenv("CHANNEL_IDS", "1385808487597998150").split(",") if c.strip()}

# bot settings
SCAN_DELAY = 0.01        # seconds to wait before checking and pinging
PING_COOLDOWN = 0.01     # seconds before the same person can be pinged again
PING_VISIBLE_TIME = 0.01 # seconds before deleting ping message

# state tracking
last_ping_time = {USER_1: 0, USER_2: 0}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    # ignore bot messages
    if message.author.bot:
        return

    # only ping in whitelisted channels
    if message.channel.id not in CHANNEL_IDS:
        return

    if message.author.id not in [USER_1, USER_2]:
        return

    # ignore replies
    if message.reference is not None:
        return

    # check who to ping
    other_user = USER_1 if message.author.id == USER_2 else USER_2

    # check cooldown for pings to that user
    now = time.time()
    if now - last_ping_time[other_user] < PING_COOLDOWN:
        return

    # scan delay
    await asyncio.sleep(SCAN_DELAY)

    # only ping if this is still the newest message in the channel
    channel = message.channel
    async for msg in channel.history(limit=1):
        if msg.id != message.id:
            return

    ping_msg = await channel.send(f"<@{other_user}>")
    await asyncio.sleep(PING_VISIBLE_TIME)
    try:
        await ping_msg.delete()
    except discord.errors.NotFound:
        pass

    # update last ping time
    last_ping_time[other_user] = now

client.run(TOKEN)
