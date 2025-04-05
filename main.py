from dotenv import load_dotenv
import os
from discord.ext import commands
import discord
from dataclasses import dataclass
import datetime
from google import genai
import textwrap
from helper import split_text_into_chunks
from collections import defaultdict, deque

load_dotenv()  # Load environment var iables from .env file

channel_message_history = defaultdict(lambda: deque(maxlen=5))


bot_token = os.getenv('BOT_TOKEN')
Channel_id=int(os.getenv("Channel_id"))
gemini_token=os.getenv("gimni_token")


bot=commands.Bot(command_prefix="!",intents=discord.Intents.all())

@dataclass
class Sessions:
    is_active: bool=False
    start_time:int =0
    end_time:int=0


session=Sessions()

@bot.event
async def on_ready():
    channel=bot.get_channel(Channel_id)
    await channel.send("HELLO! study bot is ready")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Add the new message to the channel's history
    print(message.author.name,message.content)

    channel_message_history[message.channel.id].append({
        'author': message.author.name,
        'content': message.content
    })

    # Process commands if any
    await bot.process_commands(message)




@bot.command()
async def introduce(ctx):
    await ctx.send("i'm a AI assistant bot for your help, you can ask anything to me and i will give you the AI generted Answer")
    return


@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("Session is already started")
        return
    session.is_active=True
    session.start_time=ctx.message.created_at.timestamp()
    human_readable_time=ctx.message.created_at.strftime("%H:%M:%S")

    await ctx.send(f"New Session started {human_readable_time}")


@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No Session is active!")
        return
    session.is_active=False
    end_time=ctx.message.created_at.timestamp()
    duration=end_time-session.start_time
    human_readable_duration=str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended after {human_readable_duration} seconds")

@bot.command()
async def search(ctx, *, query: str):    
    # print(query)

    history = channel_message_history[ctx.channel.id]
    context_messages = "\n".join([f"{msg['author']}: {msg['content']}" for msg in history])


    client = genai.Client(api_key=gemini_token)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=query
    )
    response_text = response.text
    if len(response_text)>=2000:
        chunks = split_text_into_chunks(response_text)
        for chunk in chunks:
            await ctx.send(chunk)
    else:
        await ctx.send(str(response_text))

    return

bot.run(bot_token)
