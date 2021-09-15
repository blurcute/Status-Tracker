# Discord
from os import name
import discord
from discord import colour
from discord.ext import commands
from discord.ext.commands.core import command
from discord.message import Message

# Slash Commands
from discord_slash import cog_ext, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ComponentType, SlashCommandOptionType, ButtonStyle
from discord_slash.utils import manage_components

# Librarys
from colorama import Fore
import datetime
import time
import json
import Utilities
import psutil
import asyncio

# -- Local Database
with open("Database/config.json", "r") as f:
    Data = json.load(f)

#Defines variables for the uptime
seconds = 0 
minutes = 0
hours = 0
days = 0

class Util(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
    
    # Logs the Cog has turned on!
    @commands.Cog.listener()
    async def on_ready(self):
        x = datetime.datetime.now()
        print(f"{Fore.GREEN}[{self.__class__.__name__}]{Fore.RESET} File Loaded! | {Fore.BLUE}[{x.strftime('%x | %X')}]{Fore.RESET}")
        global seconds
        global minutes
        global hours
        global days
        while True:
            await asyncio.sleep(1)
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
                if minutes == 60:
                    minutes = 0
                    hours += 1
                    if hours == 24:
                        hours = 0
                        days += 1

    @cog_ext.cog_slash(name="Invite", description="Invite Status Tracker to your server.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def InviteSlash(self, ctx):
        embed = discord.Embed(description=f"[Click here]({Data['Status_Tracker_Invite']}) for bot.", colour=Utilities.mainColor())
       
        Emoji_Server = self.Client.get_guild(Data['Emoji_Server'])
        Bot = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Bot_Emoji'])
        Button = [manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.URL, label=f"Invite me", emoji=Bot, url=Data['Status_Tracker_Invite']))]
        await ctx.send(embed=embed, components=Button)

    @InviteSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

    @cog_ext.cog_slash(name="Support", description="Status Tracker support Server.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def SupportSlash(self, ctx):
        embed = discord.Embed(description=f"[Click here]({Data['Support_Server']}) for support.", colour=Utilities.mainColor())

        Emoji_Server = self.Client.get_guild(Data['Emoji_Server'])
        Support = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Support_Emoji'])
        Button = [manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.URL, label="Support", emoji=Support, url=Data['Support_Server']))]
        await ctx.send(embed=embed, components=Button)

    @SupportSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

    @cog_ext.cog_slash(name="Ping", description="Let's you know if the bot is alive 🏓", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def PingSlash(self, ctx):
        before = time.monotonic()
        Ping_Message = await ctx.send(f"Pong 🏓")
        ping = (time.monotonic() - before) * 1000

        Alive_Embed = discord.Embed(color=Utilities.mainColor(), timestamp=datetime.datetime.utcnow())
        Alive_Embed.add_field(name="• Bot Latency", value=f"**`{round(self.Client.latency * 1000)}`**ms")
        Alive_Embed.add_field(name="• API Latency", value=f"**`{round(ping)}`**ms", inline=False)
        Alive_Embed.set_footer(text="Pong 😉")
        Alive_Embed.set_author(name=self.Client.user.name, icon_url=self.Client.user.avatar_url, url=Data['Support_Server'])
        Alive_Embed.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")    
        await Ping_Message.edit(content=f"**{self.Client.user.name}** having issues? use **`/support`**", embed=Alive_Embed)

    @PingSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

    @cog_ext.cog_slash(name="Stats", description="Status Tracker Information.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, read_messages=True)
    async def BotInfoSlash(self, ctx):

        # Collects all the emojis.
        Emoji_Server = self.Client.get_guild(Data['Emoji_Server'])
        Stem = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Stem_Emoji'])
        StemOver = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['StemOver_Emoji'])

        Total_Members = sum(1 for _ in self.Client.get_all_members())
        Guilds = len(self.Client.guilds)
        ramAv = pretty_size(psutil.virtual_memory().total)
        ramUs = pretty_size(psutil.virtual_memory().available)

        Stats_Embed = discord.Embed(description=f"{Stem} `Guilds: ` **|** **{Guilds}**\n{Stem} `Members:` **|** **{Total_Members}**\n{Stem} **`Ram:    `** **|** `{(ramUs)}/{(ramAv)} ({(psutil.virtual_memory().percent)}%)`\n{StemOver} **`Uptime: `** **|** `{(days)} days, {hours} hours, {minutes} minutes, {seconds} seconds`", colour=Utilities.mainColor(), timestamp=datetime.datetime.utcnow())
        Stats_Embed.set_author(name=self.Client.user.name, icon_url=self.Client.user.avatar_url, url=Data['Support_Server'])
        Stats_Embed.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}")   
        Stats_Embed.set_thumbnail(url=self.Client.user.avatar_url) 
        await ctx.send(embed=Stats_Embed)

    @BotInfoSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

    @cog_ext.cog_slash(name="Checklist", description="Check the setup and permissons.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, read_messages=True)
    async def CheckSlash(self, ctx):
        Guild = self.Client.get_guild(ctx.guild.id)
        Server = await self.Client.GUILDS.find_by_id(ctx.guild.id)

        if not Server:
            await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Manager Role": 0, "Status Role": 0, "Logging Channel": 0, "Status_text": 0})
            Server = await self.Client.GUILDS.find_by_id(ctx.guild.id)
            
        if not await Utilities.CommandPermission(self, self.Client, ctx): # Checks if they have permisson to run this command.
            return

        bot_member = Guild.me
        bot_guild_perms = bot_member.guild_permissions
        PERMISSION_LOGGER = ""
        SERVER_LOGGER = ""
       
        if bot_guild_perms.manage_roles is True:
            Checker_Text = f'**`MANAGE_ROLES   `** `|` {Data["Emojis"]["Good_Emoji"]}'
        
        else:
            Checker_Text = f'**`MANAGE_ROLES   `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.manage_webhooks is True:
            Checker_Text = f'\n**`MANAGE_WEBHOOKS`** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`MANAGE_WEBHOOKS`** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.manage_messages is True:
            Checker_Text = f'\n**`MANAGE_MESSAGES`** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`MANAGE_MESSAGES`** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.send_messages is True:
            Checker_Text = f'\n**`SEND_MESSAGES  `** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`SEND_MESSAGES  `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.read_messages is True:
            Checker_Text = f'\n**`READ_MESSAGES  `** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`READ_MESSAGES  `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.read_messages and bot_guild_perms.send_messages is True:
            Checker_Text = f'\n**`VIEW_CHANNELS  `** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`VIEW_CHANNELS  `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.external_emojis and bot_guild_perms.external_emojis is True:
            Checker_Text = f'\n**`EXTERNAL_EMOJIS`** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`EXTERNAL_EMOJIS`** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if bot_guild_perms.embed_links  is True:
            Checker_Text = f'\n**`EMBED_LINKS    `** `|` {Data["Emojis"]["Good_Emoji"]}'

        else:
            Checker_Text = f'\n**`EMBED_LINKS    `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        
        PERMISSION_LOGGER += Checker_Text

        if Server['Manager Role'] == 0: 
            Checker_Text = f'**`MANAGER_ROLE   `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        else:
            Checker_Text = f'**`MANAGER_ROLE   `** `|` {Data["Emojis"]["Good_Emoji"]}'
        
        SERVER_LOGGER += Checker_Text

        if Server['Status Role'] == 0:
            Checker_Text = f'\n**`STATUS_ROLE    `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        else:
            Checker_Text = f'\n**`STATUS_ROLE    `** `|` {Data["Emojis"]["Good_Emoji"]}'
        
        SERVER_LOGGER += Checker_Text

        if Server['Logging Channel'] == 0:
            Checker_Text = f'\n**`LOGGING_CHANNEL`** `|` {Data["Emojis"]["Bad_Emoji"]}'
        else:
            Checker_Text = f'\n**`LOGGING_CHANNEL`** `|` {Data["Emojis"]["Good_Emoji"]}'
        
        SERVER_LOGGER += Checker_Text

        Text = Server['Status_text']

        if len(str(Text)) < 2:
            Checker_Text = f'\n**`STATUS_TEXT    `** `|` {Data["Emojis"]["Bad_Emoji"]}'
        else:
            Checker_Text = f'\n**`STATUS_TEXT    `** `|` {Data["Emojis"]["Good_Emoji"]}'
        
        SERVER_LOGGER += Checker_Text
        
        CHECKER = discord.Embed(description=f"{Data['Emojis']['Good_Emoji']} - Has Permisson(s) or Setup.\n{Data['Emojis']['Bad_Emoji']} - Needs Permisson(s) or Setup.", colour=Utilities.mainColor(), timestamp=datetime.datetime.utcnow())
        CHECKER.add_field(name="• Permissions", value=PERMISSION_LOGGER)
        CHECKER.add_field(name="• Setup", value=SERVER_LOGGER, inline=False)
        CHECKER.set_author(name=self.Client.user.name, icon_url=self.Client.user.avatar_url, url=Data['Support_Server'])
        CHECKER.set_footer(text=f"{self.Client.user.name}", icon_url=f"{self.Client.user.avatar_url}") 
        CHECKER.set_thumbnail(url="https://cdn.discordapp.com/emojis/887382700095311902.png?v=1")   
        await ctx.send(embed=CHECKER)

    @CheckSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

    @cog_ext.cog_slash(name="Help", description="You need help? well you found me.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def HelpSlash(self, ctx):
        # Checks for Admin.
        if ctx.author.guild_permissions.administrator:
            # Embed
            Normal_Help_Embed = discord.Embed(description=f"You can use `/` for `{self.Client.user.name}`\nin `{ctx.guild.name}` 😊", colour=Utilities.mainColor())
            Normal_Help_Embed.add_field(name="• Useful:", value=f"[Commands List]({Data['Documentation']}dashboard/commands)\n[Support Server]({Data['Support_Server']})\n[Invite me]({Data['Status_Tracker_Invite']})")
            Normal_Help_Embed.set_author(name=f"{self.Client.user.name}", icon_url=self.Client.user.avatar_url, url=Data['Support_Server'])
            
            # Buttons
            Emoji_Server = self.Client.get_guild(Data['Emoji_Server'])
            Support = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Support_Emoji'])
            Bot = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Bot_Emoji'])
            Buttons = [manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.URL, label="Support", emoji=Support, url=Data['Support_Server']), manage_components.create_button(style=ButtonStyle.URL, label=f"Invite me", emoji=Bot, url=Data['Status_Tracker_Invite']))]
            
            await ctx.send(embed=Normal_Help_Embed, components=Buttons)

    @HelpSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix
 
def setup(Client):
    Client.add_cog(Util(Client))