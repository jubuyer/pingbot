# Bot that scans channels and pings users if new message id is detected
import discord
import asyncio
import os
import time
import re
from dotenv import load_dotenv

# load env vars
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

USER_1 = int(os.getenv("USER_1"))
USER_2 = int(os.getenv("USER_2"))
# BOT_CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))  # no longer needed

# bot settings
SCAN_DELAY = 0.01        # seconds to wait before checking and pinging
PING_COOLDOWN = 0.01     # seconds before the same person can be pinged again
PING_VISIBLE_TIME = 0.01 # seconds before deleting ping message

# state tracking
last_message_id = None
last_ping_time = {USER_1: 0, USER_2: 0}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    global last_message_id, last_ping_time  # last_ping_msg removed

    # ignore bot messages
    if message.author.bot:
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

    # save message id
    last_message_id = message.id

    # scan delay
    await asyncio.sleep(SCAN_DELAY)

    channel = message.channel
    last_msg = await channel.fetch_message(last_message_id)
    async for msg in channel.history(limit=1):
        if msg.id != last_msg.id:
            return

    ping_msg = await channel.send(f"<@{other_user}>")
    await asyncio.sleep(PING_VISIBLE_TIME)
    try:
        await ping_msg.delete()
    except discord.errors.NotFound:
        pass

    # update last ping time
    last_ping_time[other_user] = now

    # replace https://x.com or https://twitter.com links with fxtwitter links
    if "https://x.com" in message.content or "https://twitter.com" in message.content or "https://www.x.com" in message.content or "https://www.twitter.com" in message.content:
        new_content = re.sub(
            r"https://(www\.)?(x|twitter)\.com/([a-zA-Z0-9_]+)/status/([0-9]+)",
            r"https://fxtwitter.com/\3/status/\4",
            message.content
        )
        if new_content != message.content:
            match = re.search(r"https://(www\.)?(x|twitter)\.com/([a-zA-Z0-9_]+)/status/([0-9]+)", message.content)
            if match:
                original_link = f"https://{match.group(1) or ''}{'x' if match.group(2) == 'x' else 'twitter'}.com/{match.group(3)}/status/{match.group(4)}"
                button = discord.ui.Button(style=discord.ButtonStyle.link, url=original_link, label="Open in X")
                view = discord.ui.View()
                view.add_item(button)
            await message.delete()
            await message.channel.send(f"{message.author.name}: {new_content}", view=view)
        return
    
    # replace https://reddit.com links with vxreddit links
    if "https://reddit.com" in message.content or "https://www.reddit.com" in message.content:
        new_content = re.sub(
            r"https://(www\.)?reddit\.com",
            r"https://vxreddit.com",
            message.content
        )
        if new_content != message.content:
            match = re.search(r"https://(www\.)?reddit\.com[^\s]*", message.content)
            if match:
                original_link = match.group(0)
                button = discord.ui.Button(style=discord.ButtonStyle.link, url=original_link, label="Open in Reddit")
                view = discord.ui.View()
                view.add_item(button)
            await message.delete()
            await message.channel.send(f"{message.author.name}: {new_content}", view=view)
            return
    
    # replace https://tiktok.com links with tnktok links
    if "https://tiktok.com" in message.content or "https://www.tiktok.com" in message.content:
        new_content = re.sub(
            r"https://(www\.)?tiktok\.com",
            r"https://\1tnktok.com",
            message.content
        )
        if new_content != message.content:
            match = re.search(r"https://(www\.)?tiktok\.com[^\s]*", message.content)
            if match:
                original_link = match.group(0)
                button = discord.ui.Button(style=discord.ButtonStyle.link, url=original_link, label="Open in TikTok")
                view = discord.ui.View()
                view.add_item(button)
                await message.delete()
                await message.channel.send(content=f"{message.author.name}: {new_content}", view=view)
            return
            
client.run(TOKEN)