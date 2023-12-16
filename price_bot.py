from torn_client import User as TornUser
from time import sleep
import discord as ds
from discord.ext import commands
from discord import User as DiscordUser
import json

users = {} #key : discord_username,value: User
TOKEN = "MTE4NTYzNjI3MDM5NTg5MTc3NQ.GPDy7g.Rk0PRGtPMTwf7xHaCjaRA50Bf_8E0gnXgxSJD0"
intents = ds.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    #await tree.sync()#guild=discord.Object(id=my guild id)
    print("Hello, I am MisterReco's Torn Bot")

#add a user given their Torn API Key
@bot.command()
async def add_user(ctx, key):
    user = str(ctx.author)
    if user not in users:
        users[user] = TornUser(key)
        await ctx.send(f"User {user} has been added")
    else:
        await ctx.send(f"User {user} already added")
#add an item to track
@bot.command()
async def add(ctx, id, threshold):
    user = ctx.author
    threshold = int(threshold)
    if str(user) not in users:
        await ctx.send(f"User {user} not in data base, use command `add_user`")
    else:
        await ctx.send(f"Adding item #{id} with a threshold of ${threshold:,}")

#update an item currently being tracked
@bot.command()
async def update(ctx, id, threshold):
    await ctx.send(f"Updating item #{id} with a threshold of {threshold}")

#remove an item from being tracked
@bot.command()
async def remove(ctx, id):
    await ctx.send(f"Stopped tracking item #{id}")

while True:
    try:
        print("Running bot")
        bot.run(TOKEN)
    except Exception:
        print("Exception")
        #with open("users.json", "w") as fp:
        #    json.dump(users, fp)
        sleep(70)