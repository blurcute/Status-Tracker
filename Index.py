# Discord
import discord
from discord.ext import commands, tasks

# Librarys
from discord_slash import SlashCommand
from colorama import Fore
import json
import os
import asyncio
import Utilities
import datetime
import motor.motor_asyncio
from Admin.mongo import Document
from dotenv import load_dotenv

# Database.
with open("Database/config.json", "r") as f:
    Config = json.load(f)

# Loads the evn file.  
load_dotenv()

# Make the Client.
Client = commands.Bot(command_prefix=commands.when_mentioned_or(Config["Prefix"]), intents=discord.Intents.all(), case_insensitive=True, strip_after_prefix=True, owner_ids=Config["Owners"])
Client.remove_command('help')
Client.connection_url = "mongodb+srv://GiveawayUser:Giveaway2006@giveaways.kwjkn.mongodb.net/Giveaways?retryWrites=true&w=majority"
Slash = SlashCommand(Client, sync_commands=True, sync_on_cog_reload=True)

# Turns on all the files.
for File in os.listdir("./cogs"):
    if File.endswith(".py"):
        Client.load_extension(f"cogs.{File[:-3]}")

# A ready event for when Client comes online.
@Client.event
async def on_ready():
    guilds = len(Client.guilds)
    users = sum(1 for _ in Client.get_all_members())
    print(
        f"""
        {Fore.RED}                                                                                                                                                   
 ________  _________  ________  _________  ___  ___  ________           _________  ________  ________  ________  ___  __    _______   ________     
|\   ____\|\___   ___\\   __  \|\___   ___\\  \|\  \|\   ____\         |\___   ___\\   __  \|\   __  \|\   ____\|\  \|\  \ |\  ___ \ |\   __  \    
\ \  \___|\|___ \  \_\ \  \|\  \|___ \  \_\ \  \\\  \ \  \___|_        \|___ \  \_\ \  \|\  \ \  \|\  \ \  \___|\ \  \/  /|\ \   __/|\ \  \|\  \   
 \ \_____  \   \ \  \ \ \   __  \   \ \  \ \ \  \\\  \ \_____  \            \ \  \ \ \   _  _\ \   __  \ \  \    \ \   ___  \ \  \_|/_\ \   _  _\  
  \|____|\  \   \ \  \ \ \  \ \  \   \ \  \ \ \  \\\  \|____|\  \            \ \  \ \ \  \\  \\ \  \ \  \ \  \____\ \  \\ \  \ \  \_|\ \ \  \\  \| 
    ____\_\  \   \ \__\ \ \__\ \__\   \ \__\ \ \_______\____\_\  \            \ \__\ \ \__\\ _\\ \__\ \__\ \_______\ \__\\ \__\ \_______\ \__\\ _\ 
   |\_________\   \|__|  \|__|\|__|    \|__|  \|_______|\_________\            \|__|  \|__|\|__|\|__|\|__|\|_______|\|__| \|__|\|_______|\|__|\|__|
   \|_________|                                        \|_________|                                                                                
    {Fore.RESET}

{Fore.RED}[!]{Fore.RESET} Logged in as: {Client.user.name} ({Client.user.id})\n\n{Fore.RED}[!]{Fore.RESET} Prefix: {Config['Prefix']}\n\n{Fore.RED}[!]{Fore.RESET} Servers: {guilds}\n\n{Fore.RED}[!]{Fore.RESET} Users: {users}\n_____________________\n"""
    )


    await Client.change_presence(status= discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name=f"{Config['Status']}"))

    Client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(Client.connection_url))
    Client.db = Client.mongo["StatusTracker"]
    Client.GUILDS = Document(Client.db, "Guilds")
    Client.STATUS = Document(Client.db, "Statuses")
    print(f"{Fore.GREEN}[!]{Fore.RESET} Initialized Database\n_____________________")


# On Message event.
@Client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith(f"<@!{Client.user.id}>") and \
        len(message.content) == len(f"<@!{Client.user.id}>"
    
    ):
       await asyncio.sleep(1.0)
       await message.reply(f"Hi! I use **`Slash commands`**!\n> Type **`/help`** for **help**!")

    await Client.process_commands(message)

# --
@Slash.slash(name="Load", description="Load a file.", guild_ids=Config['Beta_Slash_Server'])
@commands.is_owner()
async def LoadSlash(ctx, *, module):
    try:
      Client.load_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
        await Utilities.ErrorEmbed(Client=Client, ctx=ctx, error=f"I have **Failed** to **`load`**: **{str(module).lower()}**")
    else:
        await Utilities.SuccessEmbed(Client=Client, ctx=ctx, comment=f"You have **Loaded**: **`{str(module).lower()}`**")

@LoadSlash.error
async def Slash_error(ctx, error):
    await Utilities.Command_Error(Client, ctx, commands, error)
# --
@Slash.slash(name="Unload", description="Unload a file.", guild_ids=Config['Beta_Slash_Server'])
@commands.is_owner()
async def UnloadSlash(ctx, *, module):
    try:
      Client.unload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
        await Utilities.ErrorEmbed(Client=Client, ctx=ctx, error=f"I have **Failed** to **`unload`**: **{str(module).lower()}**")
    else:
        await Utilities.SuccessEmbed(Client=Client, ctx=ctx, comment=f"You have **Unloaded**: **`{str(module).lower()}`**")

@UnloadSlash.error
async def Slash_error(ctx, error):
    await Utilities.Command_Error(Client, ctx, commands, error)
# --
@Slash.slash(name="Reload", description="Reload a file.", guild_ids=Config['Beta_Slash_Server'])
@commands.is_owner()
async def ReloadSlash(ctx, *, module):
    try:
        Client.reload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
        await Utilities.ErrorEmbed(Client=Client, ctx=ctx, error=f"I have **Failed** to **`reload`**: **{str(module).lower()}**")
    else:
        await Utilities.SuccessEmbed(Client=Client, ctx=ctx, comment=f"You have **Reloaded**: **`{str(module).lower()}`**")

@ReloadSlash.error
async def Slash_error(ctx, error):
    await Utilities.Command_Error(Client, ctx, commands, error)

# Turns on the Client.
Client.run("ODg0ODY3NTU2MTY1NDM1Mzkz.YTevIQ.B32uw4XMoy4kveIs5AKVjr-GDA8")
