# Discord
import discord
from discord import colour
from discord.ext import commands

# Slash Commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ComponentType, SlashCommandOptionType, ButtonStyle
from discord_slash.utils import manage_components

# Librarys
from colorama import Fore
import datetime
import json
import Utilities
import asyncio

# Database
with open("Database/config.json", "r") as f:
    Data = json.load(f)

class Setup(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
    
    # Logs the Cog has turned on!
    @commands.Cog.listener()
    async def on_ready(self):
        x = datetime.datetime.now()
        print(f"{Fore.GREEN}[{self.__class__.__name__}]{Fore.RESET} File Loaded! | {Fore.BLUE}[{x.strftime('%x | %X')}]{Fore.RESET}")   
    
    @cog_ext.cog_slash(name="Server", description="Manage server settings, data, permissions and more.", guild_ids=Data['Beta_Slash_Server'])
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, read_messages=True, manage_roles=True, manage_messages=True, manage_webhooks=True, external_emojis=True)
    async def ServerSlash(self, ctx):
        await ctx.defer()

        Server = await self.Client.GUILDS.find_by_id(ctx.guild.id)

        if not Server:
            await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Manager Role": 0, "Status Role": 0, "Logging Channel": 0, "Status_text": 0})
            Server = await self.Client.GUILDS.find_by_id(ctx.guild.id)

        if not await Utilities.CommandPermission(self, self.Client, ctx): # Checks if they have permisson to run this command.
            return

        # Collects all the emojis.
        Emoji_Server = self.Client.get_guild(Data['Emoji_Server'])
        Stem = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Stem_Emoji'])
        StemOver = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['StemOver_Emoji'])
        Add_Emoji = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Add_Emoji'])
        Cancel_Emoji = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Cancel_Emoji'])
        Remove_Emoji = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['Remove_Emoji'])
        News_Emoji = discord.utils.get(Emoji_Server.emojis, id=Data['Emojis']['News_Emoji'])

        # Collects Data.
        Support = Data['Support_Server']

        # Adds Discord Buttons.
        MainActionRow = [manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.gray, label="Add", emoji=Add_Emoji, custom_id="Add"), manage_components.create_button(style=ButtonStyle.gray, label="Remove", emoji=Add_Emoji, custom_id="Remove")), manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.red, label="Exist", emoji=Cancel_Emoji, custom_id="Cancel"), manage_components.create_button(style=ButtonStyle.gray, label="Show", emoji=News_Emoji, custom_id="Show"))]
        DisabledActionRow = [manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.gray, label="Add", emoji=Add_Emoji, custom_id="Add", disabled=True), manage_components.create_button(style=ButtonStyle.gray, label="Remove", emoji=Add_Emoji, custom_id="Remove", disabled=True)), manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.red, label="Exist", emoji=Cancel_Emoji, custom_id="Cancel", disabled=True), manage_components.create_button(style=ButtonStyle.gray, label="Show", emoji=News_Emoji, custom_id="Show", disabled=True))]
        
        # Sends the Embed.
        Server_Embed = discord.Embed(title=f"How to setup {self.Client.user.name}!", description=f"Here you will get the basic information on how to setup **`{self.Client.user.name}`**.\n_ _\n**• How do I update Data?**\nIf you would like to update the **`Status Role`** and more you can click the add button to get started.\n_ _\n**• How do I remove Data?**\nIf you would like to `delete/remove` data from the bot like **`Status Role`** and more you can click the remove button.", colour=Utilities.mainColor())
        Message = await ctx.send(embed=Server_Embed, components=MainActionRow)

        Settings = {
                            "Manager_Role": {"Value": None, "Description": "What should the Manager role be?", "Name": "Manager Role", "Input": "What is the Role?"}, 
                            "Status_Role": {"Value": None, "Description": "What should the Status role be?", "Name": "Status Role", "Input": "What is the Role?"},
                            "Logging_Channel": {"Value": None, "Description": "What channel should be used for logs?", "Name": "Logging Channel", "Input": "What is the Channel?"},
                            "Status_Text": {"Value": None, "Description": "What Status should members have?", "Name": "Status Text", "Input": "What is the Text?"}
                       }

        Remove = {
                            "Manager_Role": {"Value": None, "Description": "Removes Manager Role", "Name": "Manager Role", "Input": "Note: It will remove the Content."}, 
                            "Status_Role": {"Value": None, "Description": "Removes Status Role", "Name": "Status Role", "Input": "Note: It will remove the Content."},
                            "Logging_Channel": {"Value": None, "Description": "Removes Logging Channel", "Name": "Logging Channel", "Input": "Note: It will remove the Content."},
                            "Status_Text": {"Value": None, "Description": "Removes Status Text", "Name": "Status Text", "Input": "Note: It will remove the Content."}
                       }

        while True:
            try:
                Respond = await manage_components.wait_for_component(self.Client, timeout=60, components=MainActionRow, check=lambda Respond: Respond.origin_message_id == Message.id)
            except asyncio.TimeoutError:
                try:
                   await Message.edit(content="You ran out of **time**.", embed=Server_Embed, components=[])
                   return
                except:
                    return
            
            # Checks user.
            if Respond.author.id != ctx.author.id:
                await Utilities.ErrorEmbed(Client=self.Client, ctx=ctx, error="You **`DON'T`** have access to these buttons.\nYou must **run** the command to be able use them.", hidden=True)
                continue
            
            # Add Setting
            if Respond.custom_id == "Add":
                
                # If no possible settings left.
                Options = [manage_components.create_select_option(label=list(Settings.values())[Index]["Name"], value=Requirement, description=list(Settings.values())[Index]["Description"]) for Index, Requirement in enumerate(Settings) if not list(Settings.values())[Index]["Value"]]
                if not Options:
                    await Utilities.ErrorEmbed(Client=self.Client, ctx=ctx, error="There is no longer any **options**!", hidden=True)
                    await Message.edit(components=MainActionRow)
                    continue
                
                ActionRow = [manage_components.create_actionrow(manage_components.create_select(options=Options, min_values=1, max_values=1, custom_id="Add", placeholder="Select Setting")), manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.gray, label="Cancel", emoji=Remove_Emoji, custom_id="Cancel"))]
                await Respond.edit_origin(embed=Server_Embed, components=ActionRow)
                
                # Timeout for buttons
                while True:
                    try:
                        Respond = await manage_components.wait_for_component(self.Client, timeout=60, components=ActionRow, check=lambda Respond: Respond.origin_message_id == Message.id)
                    except asyncio.TimeoutError:
                        await Message.edit(content="You ran out of **time**.", embed=Server_Embed, components=[])
                        return
                    
                    # Checks User.
                    if Respond.author.id != ctx.author.id:
                        await Utilities.ErrorEmbed(Client=self.Client, ctx=ctx, error="You **`DON'T`** have access to these buttons.\nYou must **run** the command to be able use them.", hidden=True)
                        continue
                    break
                
                # Cancel 
                if Respond.custom_id == "Cancel":
                    await Respond.edit_origin(components=MainActionRow)
                    continue

                # Continues will Settings
                elif Respond.custom_id == "Add":
                    await Message.edit(components=DisabledActionRow)
                    RequirementEmbed = discord.Embed(description=Settings[Respond.data["values"][0]]["Input"], color=Utilities.mainColor())
                    RespondMessage = await Respond.send(embed=RequirementEmbed)
                    try:
                        Answer = await self.Client.wait_for("message", timeout=60, check=lambda Message: Message.author == ctx.author and Message.channel == ctx.channel)
                    except asyncio.TimeoutError:
                        await Message.edit(content="You ran out of **time**.", embed=Server_Embed, components=[])
                        await RespondMessage.delete()
                        return
                    await Answer.delete()
                    await RespondMessage.delete()
                    
                    # MANAGER ROLE
                    if Respond.data["values"][0] == "Manager_Role":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if not Server['Manager Role'] == 0:
                            RequirementEmbed = discord.Embed(description="**`MANAGER_ROLE`** is already **setup**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        for Role in ctx.guild.roles:
                            Role.name == Role.name.lower()
                        
                        # If role doesn't exist.
                        try:
                            Role = await commands.RoleConverter().convert(ctx, Answer.content)
                        except commands.errors.RoleNotFound:
                            RequirementEmbed = discord.Embed(description="I wasn't able to find this **`role`**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        # If role asked was @everyone.
                        if Role.name == "@everyone":
                            RequirementEmbed = discord.Embed(description="You can't use the role: **`@everyone`**", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        # If role asked was @here.
                        if Role.name == "@here":
                            RequirementEmbed = discord.Embed(description="You can't use the role: **`@here`**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue    

                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Manager Role": Role.id})
                    
                    # STATUS ROLE
                    if Respond.data["values"][0] == "Status_Role":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if not Server['Status Role'] == 0:
                            RequirementEmbed = discord.Embed(description="**`STATUS_ROLE`** is already **setup**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        for Role in ctx.guild.roles:
                            Role.name == Role.name.lower()
                        
                        # If role doesn't exist.
                        try:
                            Role = await commands.RoleConverter().convert(ctx, Answer.content) 
                        except commands.errors.RoleNotFound:
                            RequirementEmbed = discord.Embed(description="I wasn't able to find this **`role`**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        # If role asked was @everyone.
                        if Role.name == "@everyone":
                            RequirementEmbed = discord.Embed(description="You can't use the role: **`@everyone`**", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        # If role asked was @here.
                        if Role.name == "@here":
                            RequirementEmbed = discord.Embed(description="You can't use the role: **`@here`**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue    

                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Status Role": Role.id})
                    
                    # STATUS TEXT
                    if Respond.data["values"][0] == "Status_Text":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)
                        Text = Server['Status_text']

                        if len(str(Text)) > 2:
                            RequirementEmbed = discord.Embed(description="**`STATUS_TEXT`** is already **setup**.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue

                        if len(Answer.content) < 2:
                            RequirementEmbed = discord.Embed(description="**`STATUS_TEXT`** must be between `2-128` characters.", color=Utilities.errorColor())
                            await ctx.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                        
                        # if asked Activity had more then 128 characters.
                        if len(Answer.content) > 128:
                            RequirementEmbed = discord.Embed(description="The **`STATUS_TEXT`** can only be **128** characters or less.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue 

                        TEXT = Answer.content


                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Status_text": TEXT})
                    
                    await Message.edit(embed=Server_Embed, components=MainActionRow)
                    
                    # LOGGING CHANNEL
                    if Respond.data["values"][0] == "Logging_Channel":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if not Server['Logging Channel'] == 0:
                            RequirementEmbed = discord.Embed(description="**`LOGGING_CHANNEL`** is already **setup**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue
                
                        try:
                            Channel = await commands.TextChannelConverter().convert(ctx, str(Answer.content))
                        except commands.errors.ChannelNotFound:                 
                            RequirementEmbed = discord.Embed(description="I wasn't able to find this **`Channel`**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue

                        WEBHOOK = await Channel.create_webhook(name=f"{self.Client.user.name}", avatar=open('Images/Status-Tracker.png', 'rb').read(), reason="Webhook for logging statuses.")
                        
                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Logging Channel": Channel.id, "Webhook": WEBHOOK.url})
                    
                    await Message.edit(embed=Server_Embed, components=MainActionRow)

            elif Respond.custom_id == "Remove":
                Server = await self.Client.GUILDS.find(ctx.guild.id)
                
                # If no possible settings left.
                Options = [manage_components.create_select_option(label=list(Remove.values())[Index]["Name"], value=Requirement, description=list(Remove.values())[Index]["Description"]) for Index, Requirement in enumerate(Remove) if not list(Remove.values())[Index]["Value"]]
                if not Options:
                    await Utilities.ErrorEmbed(Client=self.Client, ctx=ctx, error="There is no longer any **options**!", hidden=True)
                    await Message.edit(components=MainActionRow)
                    continue

                ActionRow = [manage_components.create_actionrow(manage_components.create_select(options=Options, min_values=1, max_values=1, custom_id="Remove", placeholder="Remove Item")), manage_components.create_actionrow(manage_components.create_button(style=ButtonStyle.gray, label="Cancel", emoji=Remove_Emoji, custom_id="Cancel"))]
                await Respond.edit_origin(embed=Server_Embed, components=ActionRow)
                
                # Timeout for buttons
                while True:
                    try:
                        Respond = await manage_components.wait_for_component(self.Client, timeout=60, components=ActionRow, check=lambda Respond: Respond.origin_message_id == Message.id)
                    except asyncio.TimeoutError:
                        await Message.edit(content="You ran out of **time**.", embed=Server_Embed, components=[])
                        return
                    
                    # Checks User.
                    if Respond.author.id != ctx.author.id:
                        await Utilities.ErrorEmbed(Client=self.Client, ctx=ctx, error="You **`DON'T`** have access to these buttons.\nYou must **run** the command to be able use them.", hidden=True)
                        continue
                    break
                
                # Cancel 
                if Respond.custom_id == "Cancel":
                    await Respond.edit_origin(components=MainActionRow)
                    continue

                # Remove Items
                elif Respond.custom_id == "Remove":
                    await Message.edit(components=DisabledActionRow)
                    
                    # MANAGER ROLE
                    if Respond.data["values"][0] == "Manager_Role":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if  Server['Manager Role'] == 0:
                            RequirementEmbed = discord.Embed(description="**`MANAGER_ROLE`** is not **setup**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue 

                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Manager Role": 0})
                        RequirementEmbed = discord.Embed(description="I have removed **`MANAGER_ROLE`**.", color=Utilities.errorColor())
                        await Respond.send(embed=RequirementEmbed, hidden=True)
                        await Message.edit(components=MainActionRow)
                        continue
                   
                    await Message.edit(embed=Server_Embed, components=MainActionRow)
                    
                    # STATUS ROLE
                    if Respond.data["values"][0] == "Status_Role":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if Server['Status Role'] == 0:
                            RequirementEmbed = discord.Embed(description="**`STATUS_ROLE`** is not **setup**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue  

                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Status Role": 0})
                        RequirementEmbed = discord.Embed(description="I have removed **`STATUS_ROLE`**.", color=Utilities.errorColor())
                        await Respond.send(embed=RequirementEmbed, hidden=True)
                        await Message.edit(components=MainActionRow)
                        continue
                    
                    await Message.edit(embed=Server_Embed, components=MainActionRow)
                    
                    # STATUS TEXT
                    if Respond.data["values"][0] == "Status_Text":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)
                        Text = Server['Status_text']

                        if len(str(Text)) < 2:
                            RequirementEmbed = discord.Embed(description="**`STATUS_TEXT`** is not **setup**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue

                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Status_text": 0})
                        RequirementEmbed = discord.Embed(description="I have removed **`STATUS_TEXT`**.", color=Utilities.errorColor())
                        await Respond.send(embed=RequirementEmbed, hidden=True)
                        await Message.edit(components=MainActionRow)
                        continue
                    
                    await Message.edit(embed=Server_Embed, components=MainActionRow)
                    
                    # LOGGING CHANNEL
                    if Respond.data["values"][0] == "Logging_Channel":
                        Server = await self.Client.GUILDS.find(ctx.guild.id)

                        if Server['Logging Channel'] == 0:
                            RequirementEmbed = discord.Embed(description="**`LOGGING_CHANNEL`** is not **setup**.", color=Utilities.errorColor())
                            await Respond.send(embed=RequirementEmbed, hidden=True)
                            await Message.edit(components=MainActionRow)
                            continue

                        await self.Client.GUILDS.unset({"_id": ctx.guild.id, "Webhook": 0})
                        await self.Client.GUILDS.upsert({"_id": ctx.guild.id, "Logging Channel": 0})
                        RequirementEmbed = discord.Embed(description="I have removed **`LOGGING_CHANNEL`**.", color=Utilities.errorColor())
                        await Respond.send(embed=RequirementEmbed, hidden=True)
                        await Message.edit(components=MainActionRow)
                        continue
                    
                    await Message.edit(embed=Server_Embed, components=MainActionRow)        
       
                
            elif Respond.custom_id == "Show":
                Server_Show = await self.Client.GUILDS.find(ctx.guild.id)
                Settings_Text = ""

                if Server_Show['Manager Role'] == 0:
                    Manager_Text = f'{Stem} **`Manager Role:`** [`No Role currently.`]({Support})'
                else:
                    ManagerRole = ctx.guild.get_role(Server_Show['Manager Role'])
                    Manager_Text = f"{Stem} **`Manager Role:`** {ManagerRole.mention}"
                
                Settings_Text += Manager_Text
                # - - 
                if Server_Show['Status Role'] == 0:
                    Status_Role_Text = f'\n{Stem} **`Status Role:`** [`No Role currently.`]({Support})'
                else:
                    StatusRole = ctx.guild.get_role(Server_Show['Status Role'])
                    Status_Role_Text = f"\n{Stem} **`Status Role:`** {StatusRole.mention}"
                
                Settings_Text += Status_Role_Text
                # - - 
                if Server_Show['Logging Channel'] == 0:
                    Logging_Text = f'\n{Stem} **`Logging Channel:`** [`No Channel currently.`]({Support})'
                else:
                    LoggingChannel = ctx.guild.get_channel(Server_Show['Logging Channel'])
                    Logging_Text = f"\n{Stem} **`Logging Channel:`** {LoggingChannel.mention}"
                
                Settings_Text += Logging_Text 
                # - - 
                Text = Server_Show['Status_text']

                if len(str(Text)) < 2:
                    Status_Text = f'\n{StemOver} **`Status:`** [`No Text currently.`]({Support})'
                else:
                    Status_Text = f"\n{StemOver} **`Status:`** {Text}"
               
                Settings_Text += Status_Text
                
                Show_Embed = discord.Embed(description=Settings_Text, colour=Utilities.mainColor())
                await Respond.send(embed=Show_Embed, hidden=True)          
                await Message.edit(components=MainActionRow)    
    
            elif Respond.custom_id == "Cancel":
              OverEmbed = discord.Embed(title=f"{self.Client.user.name} Settings", description=f"I have updated all settings, run `/checklist` to see.", colour=Utilities.successColor())
              await Message.edit(embed=OverEmbed, components=[])   
              return 

    @ServerSlash.error
    async def Slash_error(self, ctx, error):
        await Utilities.Command_Error(self.Client, ctx, commands, error)

def setup(Client):
    Client.add_cog(Setup(Client))