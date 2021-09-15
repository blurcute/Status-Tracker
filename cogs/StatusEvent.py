# Discord
import asyncio
from typing import Text
import discord
from discord.ext import commands

# Librarys
from colorama import Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import json

# Database
with open("Database/config.json", "r") as f:
    Data = json.load(f)

class Statuses(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
    
    # Logs the Cog has turned on!
    @commands.Cog.listener()
    async def on_ready(self):
        x = datetime.datetime.now()
        print(f"{Fore.GREEN}[{self.__class__.__name__}]{Fore.RESET} File Loaded! | {Fore.BLUE}[{x.strftime('%x | %X')}]{Fore.RESET}")   
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before == None:
            return
        
        try:
            Server = await self.Client.GUILDS.find_by_id(after.guild.id)

            if not Server:
              await self.Client.GUILDS.upsert({"_id": after.guild.id, "Manager Role": 0, "Status Role": 0, "Logging Channel": 0, "Status_text": 0})
              Server = await self.Client.GUILDS.find_by_id(after.guild.id)
        except:
            return
       
        User = after

        try:
            if Server['Status Role'] == 0 or None:
                return

            if Server['Status_text'] == 0 or None:
                return
        except:
            return

        Role_ID = Server['Status Role']
        Role = discord.utils.get(User.guild.roles, id=Role_ID) 
        Status = Server['Status_text']
   
        try:
            if User.activities[0].name == None:
              if Role in User.roles:
                await asyncio.sleep(2)
                await User.remove_roles(Role, reason=f'Must have "{Status}" in Status.')

                if Server['Logging Channel'] == 0:
                    return
                
                await asyncio.sleep(2.5)
                webhook = DiscordWebhook(url=Server['Webhook'], rate_limit_retry=True)
                LOGGER = DiscordEmbed(description=f'**User:** {User.mention}\n**Action:** {Role.mention} removed.\n**Reason:** `{Status}` not in status.', color='ba7550')
                LOGGER.set_author(name='Status Updated', url=Data['Support_Server'], icon_url='https://cdn.discordapp.com/emojis/885133025338339348.png?v=1')
                LOGGER.set_timestamp()
                LOGGER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")    
                webhook.add_embed(LOGGER)
                response = webhook.execute()
                return

              else:
                return
        except:
            return
        
        await asyncio.sleep(2)

        if Status and (not len(User.activities) or not Status in User.activities[0].name):

            if Role in User.roles:
                await asyncio.sleep(2)
                await User.remove_roles(Role, reason=f'Must have "{Status}" in Status.')

                if Server['Logging Channel'] == 0:
                    return
                
                try:
                    await asyncio.sleep(2.5)
                    webhook = DiscordWebhook(url=Server['Webhook'], rate_limit_retry=True)
                    LOGGER = DiscordEmbed(description=f'**User:** {User.mention}\n**Action:** {Role.mention} removed.\n**Reason:** `{Status}` not in status.', color='ba7550')
                    LOGGER.set_author(name='Status Updated', url=Data['Support_Server'], icon_url='https://cdn.discordapp.com/emojis/885133025338339348.png?v=1')
                    LOGGER.set_timestamp()
                    LOGGER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")                     
                    webhook.add_embed(LOGGER)
                    response = webhook.execute()
                except:
                    return

            else:
                return

        else: 
            if Role in User.roles:
                return
            
            await asyncio.sleep(1)
            await User.add_roles(Role, reason=f'User has "{Status}" in Status.')

            if Server['Logging Channel'] == 0:
                return
                
            try:
                await asyncio.sleep(2.5)
                webhook = DiscordWebhook(url=Server['Webhook'], rate_limit_retry=True)
                LOGGER = DiscordEmbed(description=f'**User:** {User.mention}\n**Action:** {Role.mention} added.\n**Reason:** `{Status}` in status.', color='5090ba')
                LOGGER.set_author(name='Status Updated', url=Data['Support_Server'], icon_url='https://cdn.discordapp.com/emojis/885133025338339348.png?v=1')
                LOGGER.set_timestamp()
                LOGGER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")               
                webhook.add_embed(LOGGER)
                response = webhook.execute()
            except:
                return
        

def setup(Client):
    Client.add_cog(Statuses(Client))