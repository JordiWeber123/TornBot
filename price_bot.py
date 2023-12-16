from torn_client import User
from time import sleep
import discord as ds
from discord.ext import commands

users = {} #key : discord_username,value: User
TOKEN = ""
client = ds.Client()
intents = ds.Intents.default()

bot = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    #await tree.sync()#guild=discord.Object(id=my guild id)
    print("Hello, I am MisterReco's Torn Bot")

#add an item to track
@bot.command()
async def add(ctx, id, threshold):
    await ctx.send(f"Adding item {id} with a threshold of {threshold}")

#update an item currently being tracked
@bot.command()
async def update(ctx, id, threshold):
    await ctx.send(f"Updating item {id} with a threshold of {threshold}")

#remove an item from being tracked
@bot.command()
async def remove(ctx, id):
    await ctx.send(f"Stopped tracking item {id}")

while True:
    try:
        bot.run(TOKEN)
    except Exception:
        sleep(70)