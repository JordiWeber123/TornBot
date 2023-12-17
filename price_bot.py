from torn_client import User as TornUser
from time import sleep
import discord as ds
from discord.ext import tasks, commands
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
    check_prices.start()

#add a user given their Torn API Key
@bot.command()
async def add_user(ctx, key):
    user = str(ctx.author.id)
    if user not in users:
        users[user] = TornUser(key)
        await ctx.send(f"User @{ctx.author.id} has been added")
    else:
        await ctx.send(f"User @{ctx.author.id} already added")
#add an item to track
@bot.command()
async def add(ctx, id, threshold):
    user = str(ctx.author.id)
    id = int(id)
    threshold = int(threshold)
    if user not in users:
        await ctx.send(f"User @{ctx.author.id} not in data base, use command `add_user`")
    else:
        users[user].update_threshold(id, threshold)
        await ctx.send(f"Adding item #{id} with a threshold of ${threshold:,}")

#update an item currently being tracked
@bot.command()
async def update(ctx, id, threshold):
    user = str(ctx.author.id)
    threshold = int(threshold)
    id = int(id)
    if user not in users:
        await ctx.send(f"User @{ctx.author.id} not in data base, use command `add_user`")
    else:
        users[user].update_threshold(id, threshold)
        await ctx.send(f"Updating item #{id} with a threshold of {threshold}")

#remove an item from being tracked
@bot.command()
async def remove(ctx, id):
    id = int(id)
    user = str(ctx.author.id)
    if await check_user(ctx,user):
        torn_user = users[user]
        if torn_user.check_added(id):
            torn_user.remove(id)
            await ctx.send(f"Stopped tracking item #{id}")
        else:
            await ctx.send(f"Item #{id} is not currently being tracked")
@bot.command()
async def list_items(ctx):
    user = str(ctx.author.id)
    if await check_user(ctx, user):
        await ctx.send(f"These are the items user @{user} is currently tracking")
        list_items = "ID \tThreshold"
        listed_items += users[user].list_items()
        #TODO Make an embed instead of send
        await ctx.send(listed_items)
@bot.command()
async def dm(ctx):
    channel = await bot.create_dm(ds.Object(235894085922193408))
    await channel.send("This is a dm")
async def check_user(ctx, user_id):
    if user_id not in users:
        await ctx.send(f"User @{ctx.author.id} not in data base, use command `add_user`")
        return False
    return True



@tasks.loop(seconds=30)
async def check_prices():
    for id, torn_user in users.items(): 
        print(f"Checking key {torn_user.key}")
        message = (torn_user.check_items())
        if len(message) > 0:
            channel = await bot.create_dm(ds.Object(int(id)))
            await channel.send(message)


while True:
    try:
        print("Running bot")
        bot.run(TOKEN)
    except Exception:
        print("Exception")
        with open("users.json", "w") as fp:
            json.dump(users, fp)
        sleep(70)