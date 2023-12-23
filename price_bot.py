from torn_client import User as TornUser
from time import sleep
import discord as ds
from discord.ext import tasks, commands
from discord import User as DiscordUser
import os
from dotenv import load_dotenv
from mongo_driver import get_database, user_to_db, alreadyExists
import pymongo 
load_dotenv()
users = {} #key : discord_username,value: User
TOKEN = os.environ["DS_TOKEN"]
intents = ds.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
database = get_database()
users_collection = database["users"]
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
        temp_TornUser = TornUser(key)
        users[user] = temp_TornUser
        await ctx.send(f"User <@{ctx.author.id}> has been added")
        if not add_to_db(user, temp_TornUser):
            print("Failed to add user: user is already in database")
    else:
        await ctx.send(f"User <@{ctx.author.id}> already added")
@bot.command()
async def remove_user(ctx):
    user = str(ctx.author.id)
    if await check_user(ctx, user):
        del users[user]
        await ctx.send(f"User @<{user}> has been removed from the database")
        delete_from_db(user)
        
#add an item to track
@bot.command()
async def add(ctx, id, threshold):
    user = str(ctx.author.id)
    id = int(id)
    threshold = int(threshold)
    if await check_user(ctx, user):
        users[user].add_item(id, threshold)
        await ctx.send(f"Adding item #{id} with a threshold of ${threshold:,}")
        update_db(user)

#update an item currently being tracked
@bot.command()
async def update(ctx, id, threshold):
    user = str(ctx.author.id)
    id = int(id)
    threshold = int(threshold)
    if await check_user(ctx, user):
        users[user].update_threshold(id, threshold)
        await ctx.send(f"Updating item #{id} with a threshold of {threshold}")
        update_db(user)

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
            update_db(user)
        else:
            await ctx.send(f"Item #{id} is not currently being tracked")
@bot.command()
async def list_items(ctx):
    user = str(ctx.author.id)
    if await check_user(ctx, user):
        if len(user[user]) <= 0:
            await ctx.send(f"User <@{user} is currently not tracking any items")
            return
        await ctx.send(f"These are the items user <@{user}> is currently tracking")
        list_items = "ID \tThreshold"
        listed_items += users[user].list_items()
        #TODO Make an embed instead of send
        await ctx.send(listed_items)
@bot.command()
async def dm(ctx):
    channel = await bot.create_dm(ds.Object(ctx.author.id))
    await channel.send("This is a dm")

async def check_user(ctx, user_id):
    if user_id not in users:
        await ctx.send(f"User <@{user_id}> not in data base, use command `add_user` to add a user")
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


def load_from_db() -> dict:
    """Returns a dict from the Mongo Collection \"users\""""
    return {user["_id"]: TornUser(user["user_data"]) for user in users_collection.find()}

def add_to_db(user_id: str, torn_user: TornUser) -> bool:
    """Adds a user to the user_data collection
    
    :Parameters:
    `user_id`: the id of the user to add
    `torn_user`: a TornUser object corresponding to the user to be added"""
    if alreadyExists(user_id, users_collection): 
        return False
    users_collection.insert_one(user_to_db(user_id, torn_user))
    return True
def delete_from_db(user_id: str)-> bool:
    """Deletes a user from the user_data collection
    
    :Parameters: 
    `user_id`: the id of the user to remove"""
    if not alreadyExists(user_id, users_collection):
        return False
    query = {"_id": user_id}
    users_collection.delete_one(query)
def update_db(user_id: str):
    """Updates the user_data collection with the new user's data
    
    :Parameters:
    `user_id`: the id of the user to update"""
    query = {"_id": user_id}
    new_data = {"$set": {"user_data":  users[user_id].as_mongodoc()}}
    users_collection.update_one(query, new_data)
  
if __name__ == "__main__":
    while True:
        try:
            print("Running bot")
            users = load_from_db()
            bot.run(TOKEN)
        except Exception:
            print("Exception")
            sleep(70)