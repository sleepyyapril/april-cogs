import discord

from redbot.core import checks, commands, app_commands

data = {
    "Address": "ss14://51.222.244.125:1212",
    "Message": ""
}

class prebase_redial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "SS14Token "}

    @commands.command()
    @checks.admin()
    async def start_event(self, ctx, event_description: str):
        """
        Starts an event on prebase.
        """
        await ctx.send(f"Starting an event: {event_description}", ephemeral=True)

    @commands.command()
    @checks.admin()
    async def clear_events(self, ctx):
        """
        Clears any event on prebase.
        """
        await ctx.send.send_message("Clearing any events.", ephemeral=True)