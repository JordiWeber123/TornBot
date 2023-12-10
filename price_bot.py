from torn_client import User
import discord as ds
users = {} #key : discord_username,value: User

intents = ds.Intents.default()

client = ds.Client(intents=intents)
command_tree = ds.app_commands.CommandTree(client)
@client.event
async def on_ready():
    await tree.sync()#guild=discord.Object(id=my guild id)
    print("Hello, I am MisterReco's Torn Bot")

@command_tree.command(name="add", description="Add an item id and a threshold price")
async def first_command(interaction):
    await interaction.response.send_message("Adding...")


@client_event
async def on_message(message):
    pass
