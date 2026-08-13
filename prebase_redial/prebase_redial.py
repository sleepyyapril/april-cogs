import discord

from redbot.core import commands, app_commands

data = {
    "Address": "ss14://51.222.244.125:1212",
    "Message": ""
}

class prebase_redial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "SS14Token "}

    @app_commands.command()
    @app_commands.admin()
    @app_commands.describe(event_description="A summary of the event.")
    async def start_event(self, interaction: discord.Interaction, event_description: str):
        await interaction.response.send_message(f"Starting an event: {event_description}", ephemeral=True)

    @app_commands.command()
    @app_commands.admin()
    async def clear_events(self, interaction: discord.Interaction):
        await interaction.response.send_message("Clearing any events.", ephemeral=True)