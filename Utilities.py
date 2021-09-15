import discord
import json
import asyncio
import datetime
from discord.ext.commands.errors import BotMissingPermissions

# --
with open("Database/config.json", "r") as f:
    Data = json.load(f)

# Success Colour
def successColor():
    return 0x04d275

# Error Colour
def errorColor():
    return 0xe24b4b

# Main Colour
def mainColor():
    return 0xcf5e47

# Error Embed 
async def ErrorEmbed(Client, ctx, error, hidden = False):
    Error_Embed = discord.Embed(description=error, colour=errorColor())
    Error_Embed.set_author(name="Error", icon_url=Data['Emoji_links']['Bad_Emoji_link'])
    Error_Embed.set_footer(text=f"{Client.user.name}", icon_url=Client.user.avatar_url)
    await ctx.send(embed=Error_Embed, hidden=hidden)

# Success Embed 
async def SuccessEmbed(Client, ctx, comment, hidden = False):
    Error_Embed = discord.Embed(description=comment, colour=successColor())
    Error_Embed.set_author(name="Success", icon_url=Data['Emoji_links']['Good_Emoji_link'])
    Error_Embed.set_footer(text=f"{Client.user.name}", icon_url=Client.user.avatar_url)
    await ctx.send(embed=Error_Embed, hidden=hidden)

# Error Handler
async def Command_Error(Client, ctx, commands, error):
    await asyncio.sleep(1)

    # Discord.py errors 
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.MissingRequiredArgument):
        return await ErrorEmbed(Client=Client, ctx=ctx, error="You are **`MISSING REQUIRED ARGUMET(s)`**")

    elif isinstance(error, commands.NotOwner):
        return await ErrorEmbed(Client=Client, ctx=ctx, error=f"You don't **own** **`{Client.user.name}`**.")

    elif isinstance(error, commands.NoPrivateMessage):
        return

    elif isinstance(error, BotMissingPermissions):

        Guild = Client.get_guild(ctx.guild.id)
        bot_member = Guild.me
        bot_guild_perms = bot_member.guild_permissions
        PERMISSION_LOGGER = ""
       
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
        
        CHECKER = discord.Embed(description=f"These are the permissons the bot has though the role, Make sure to check channel permissions.\n{Data['Emojis']['Good_Emoji']} - Has Permisson(s) or Setup.\n{Data['Emojis']['Bad_Emoji']} - Needs Permisson(s) or Setup.", colour=mainColor(), timestamp=datetime.datetime.now())
        CHECKER.add_field(name="• Permissions", value=PERMISSION_LOGGER)
        CHECKER.set_author(name=Client.user.name, icon_url=Client.user.avatar_url, url=Data['Support_Server'])
        CHECKER.set_footer(text=f"{Client.user.name}", icon_url=f"{Client.user.avatar_url}")  
        try:
            await ctx.author.send(embed=CHECKER)
        except:
            return

    elif isinstance(error, commands.CheckFailure):
        return await ErrorEmbed(Client=Client, ctx=ctx, error=f"You don't have the correct **`PERMMISONS`**.")

    elif isinstance(error, commands.CommandOnCooldown):
        return await ErrorEmbed(Client=Client, ctx=ctx, error=f"This command is **ratelimited**, please try again in `{round(error.retry_after, 2)} seconds`")

    # Non Discord.py errors
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.errors.Forbidden):
            pass
        elif isinstance(error.original, asyncio.TimeoutError):
            return await ErrorEmbed(Client=Client, ctx=ctx, error=f"You have **`taken`** to long to **respond**!")
        else:
            raise error

    else:
        raise error
#        try:
#            return await ErrorEmbed(Client=Client, ctx=ctx, error=f"```py\n{error}```")
#        except:
#            return

# Permisssion check.
async def CommandPermission(self, Client, Context):
    Guild = self.Client.get_guild(Context.guild.id)
    Server = await self.Client.GUILDS.find_by_id(Context.guild.id)

    if not Server:
        await self.Client.GUILDS.upsert({"_id": Context.guild.id, "Manager Role": 0, "Status Role": 0, "Logging Channel": 0, "Status_text": 0})
        Server = await self.Client.GUILDS.find_by_id(Context.guild.id)

    if Server['Manager Role'] == 0:
        if not Context.author.guild_permissions.administrator:
            await ErrorEmbed(Client=Client, ctx=Context, error=f"You need **Administrator**.")
            return False
        
        return True
    
    else:
        Role = discord.utils.get(Context.guild.roles, id=Server['Manager Role'])
        if not Role:
            await ErrorEmbed(Client=Client, ctx=Context, error="I can't find the required role.")
            return False
        elif not Role in Context.author.roles:
            await ErrorEmbed(Client=Client, ctx=Context, error=f"You need {Role.mention}.")
            return False
    return True

