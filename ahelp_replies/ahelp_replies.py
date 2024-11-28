import aiohttp
import asyncio
import discord
from discord import ChannelType, Message
import json
from redbot.core import checks, commands, Config
from red_commons.logging import getLogger

log = getLogger("red.april-cogs.ahelpreplies")
starter_messages = {}

# Input class for the discord modal
class Input(discord.ui.Modal, title='Input server details'):
    identifier = discord.ui.TextInput(label='Server Identifier', placeholder='grimbly', required=True)
    display_name = discord.ui.TextInput(label='Display Name',
                                 placeholder='Grimbly Station',
                                 required = True)
    server_ip = discord.ui.TextInput(label='Server IP',
                                 placeholder='localhost:1212',
                                 required=True)
    token = discord.ui.TextInput(label='API Token',
                                 placeholder='Server\'s api.token value in server_config.toml',
                                 required = True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Processing...", ephemeral=True)
        self.stop()

# Button to bring up the modal
class Button(discord.ui.View):
    def __init__(self, member):
        self.member = member
        super().__init__()
        self.modal = None

    @discord.ui.button(label='Add', style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member != interaction.user:
            return await interaction.response.send_message("You cannot use this.", ephemeral=True)

        self.modal = Input()
        await interaction.response.send_modal(self.modal)
        await self.modal.wait()
        self.stop()

ACTION_TIMEOUT = 5

async def get_user_id(session: aiohttp.ClientSession, username) -> str | None:
    async with session.post(f"https://auth.spacestation14.com/api/query/name?name={username}") as resp:
        if resp.status == 404:
            return
        
        response = await resp.text()
        print(response)
        json_data = json.loads(response)
        return json_data

async def send_reply(session: aiohttp.ClientSession, server, username: str) -> tuple[int, str] | None:
    userId = await asyncio.wait_for(
        get_user_id(session, username), 
        timeout=ACTION_TIMEOUT
    )

    if userId == None:
        log.warning("No userId found.")
        return

    async def load() -> tuple[int, str]:
        async with session.post(
                server["ip_address"] + "/admin/actions/send_bwoink",
                auth=aiohttp.BasicAuth("SS14Token", server.token),
                data=b'{"Guid": user, "Text": "(DC) [color=lightblue]Name:[/color] Test", "useronly": false }'
            ) as resp:
            return resp.status, await resp.text()

    return await asyncio.wait_for(
        load(), 
        timeout=ACTION_TIMEOUT
    )

class ahelp_replies(commands.Cog):
    """AHelp replies for discord-game communication."""

    cached: dict[int, str] = {}

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier = 683728)

        default_guild = {
            "channels": {},
            "servers": {},
        }

        self.config.register_guild(**default_guild, force_registration=True)
        self.bot = bot
    
    async def handle_thread(self, message: Message, starter_message: Message, cur_server) -> None:
        first_parenthesis = message.author.name.find("(")
        username = starter_message.author.name

        if first_parenthesis != -1:
            username = starter_message.author.name[:first_parenthesis - 2]

        if username.isspace():
            print("oh")
            return
        
        async with aiohttp.ClientSession() as session:
            try:
                status, response = await send_reply(session, cur_server, username)

                if status != 200:
                    await message.channel.send(f"Failed:\n{status}: {response}")
                else:
                    await message.add_reaction('👍')
            except asyncio.TimeoutError:
                    await message.channel.send("Server timed out.")
                    return

            except Exception:
                await message.channel.send(
                    f"An Unknown error occured while trying to request this server to update, Logging to console...")
                
                log.exception(f'An error occurred while trying to reply on server **{cur_server["display_name"]}.')
                return

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild == None:
            print("test")
            return

        guild_settings = self.config.guild(message.guild)

        servers = await guild_settings.servers()
        channels = await guild_settings.channels()

        if servers is None or channels is None:
            print("settings are missing")
            return

        channel_to_use = message.channel

        if channel_to_use.type == ChannelType.public_thread:
            if channel_to_use.starter_message == None or channel_to_use.starter_message.channel == None:
                await message.channel.send("The starter message or channel could not be found. \nWhile I may add support for fetching it in the future, you have to use the command !sendmessage to reply to this ahelp.")
                return
            channel_to_use = channel_to_use.starter_message.channel

        if channels.get(str(channel_to_use.id)) == None:
            print("Channel is missing")
            return
        
        server_id = channels[str(channel_to_use.id)]

        if not server_id in servers:
            print("server is missing")
            return
        
        cur_server = servers[server_id]
        
        if message.author.bot == True and message.webhook_id == None:
            return
        
        if message.channel.type == ChannelType.public_thread:
            print("using threads")
            return await self.handle_thread(message, message.channel.starter_message, cur_server)

        if message.webhook_id == None:
            return

        if channel_to_use.type != ChannelType.text:
            return
        
        await message.create_thread(name = "Replies")

    @commands.hybrid_group()
    @checks.admin()
    async def ahrcfg(self, ctx: commands.Context) -> None:
        """
        Commands for configuring the ahelp replies cog.
        """
        pass

    @ahrcfg.command()
    async def add(self, ctx: commands.Context) -> None:
        """
        Adds a server.
        """
        view = Button(member = ctx.author)

        await ctx.send("To add a server press this button.", view=view)
        await view.wait()

        if view.modal is None:
            return

        async with self.config.guild(ctx.guild).servers() as cur_servers:
            if view.modal.identifier.value in cur_servers:
                await ctx.send("A server with that name already exists.")
                return

            cur_servers[view.modal.identifier.value] = {
                "server_ip": view.modal.server_ip.value,
                "display_name": view.modal.display_name.value,
                "token": view.modal.token.value
            }

        await ctx.send("Server added successfully.")

    @ahrcfg.command()
    async def use_channel(self, ctx: commands.Context, identifier: str) -> None:
        """
        Sets this channel as the one to watch for AHelp relays from.
        """

        servers = await self.config.guild(ctx.guild).servers()
        
        if len(servers) == 0 or not identifier in servers:
            await ctx.send("No server matching that identifier was found.")
            return

        async with self.config.guild(ctx.guild).channels() as channels:
            channels[str(ctx.channel.id)] = identifier

        await ctx.send(f'Successfully set AHelp relay channel to <#{ctx.channel.id}> for **{servers[identifier]["display_name"]}**!')

    @ahrcfg.command()
    async def list(self, ctx: commands.Context):
        """
        Lists all servers associated with this guild without exposing sensitive information.
        """

        guild_config = self.config.guild(ctx.guild)
        servers = await guild_config.servers()
        
        if len(servers) == 0:
            await ctx.send(f"No servers are associated with ``{ctx.guild.name}``")
            return
        
        servers_msg = "Servers:"

        for identifier, server in servers.items():
            servers_msg += f'\n``{server["display_name"]}``, identified as ``{identifier}``'
        
        ctx.send(servers_msg)

        


