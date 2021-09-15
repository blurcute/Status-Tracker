# Discord
import discord
from discord.ext import commands

# Librarys
from colorama import Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import json
import asyncio

# Database
with open("Database/config.json", "r") as f:
    Data = json.load(f)

class Guilds(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
    
    # Logs the Cog has turned on!
    @commands.Cog.listener()
    async def on_ready(self):
        x = datetime.datetime.now()
        print(f"{Fore.GREEN}[{self.__class__.__name__}]{Fore.RESET} File Loaded! | {Fore.BLUE}[{x.strftime('%x | %X')}]{Fore.RESET}")   
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await asyncio.sleep(2.5)
        await self.Client.GUILDS.upsert({"_id": guild.id, "Manager Role": 0, "Status Role": 0, "Logging Channel": 0, "Status_text": 0})
        await asyncio.sleep(2.5)
        webhook = DiscordWebhook(url=Data['Logging']['Guilds'], rate_limit_retry=True)
        LOGGER = DiscordEmbed(description=f'**Server:** `{guild.name}` `({guild.id})`\n**Action:** Guild added.\n**Total Guilds:** `{len(self.Client.guilds)}`.', color='5090ba')
        LOGGER.set_author(name='Guild Update', url=Data['Support_Server'], icon_url='https://cdn.discordapp.com/emojis/885133025338339348.png?v=1')
        LOGGER.set_timestamp()
        LOGGER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")    
        webhook.add_embed(LOGGER)
        response = webhook.execute()
        return
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):    
        await asyncio.sleep(2.5)
        await self.Client.GUILDS.delete_by_id(guild.id)
        await asyncio.sleep(2.5)
        webhook = DiscordWebhook(url=Data['Logging']['Guilds'], rate_limit_retry=True)
        LOGGER = DiscordEmbed(description=f'**Server:** `{guild.name}` `({guild.id})`\n**Action:** Guild removal.\n**Total Guilds:** `{len(self.Client.guilds)}`.', color='ba7550')
        LOGGER.set_author(name='Guild Update', url=Data['Support_Server'], icon_url='https://cdn.discordapp.com/emojis/885133025338339348.png?v=1')
        LOGGER.set_timestamp()
        LOGGER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")    
        webhook.add_embed(LOGGER)
        response = webhook.execute()
        return
    
def setup(Client):
    Client.add_cog(Guilds(Client))