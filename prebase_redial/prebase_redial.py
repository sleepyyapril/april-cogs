import discord
import requests

from redbot.core import checks, commands, app_commands

class prebase_redial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.admin()
    async def start_event(self, ctx, event_message: str):
        """
        Starts an event.
        """

        keys = await self.bot.get_shared_api_tokens("events")
        prebase_url = keys.get("prebase_url")
        token = keys.get("prebase_token")
        address = keys.get("events_server")

        if prebase_url is None:
            return await ctx.reply("Prebase URL not found.")

        if token is None:
            return await ctx.reply("Prebase API token not found.")

        if address is None:
            return await ctx.reply("Events server direct IP not found.")

        url = f"{prebase_url}/admin/actions/setredial"
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"SS14Token {token}"}
        data = {
            "Address": f"{address}",
            "Message": f"{event_message}"
        }

        response = requests.post(url, headers=headers, json=data)
        return await ctx.reply(f"Starting an event with message: ``{event_message}``")

    @commands.command()
    @checks.admin()
    async def clear_events(self, ctx):
        """
        Clears any event on prebase.
        """

        keys = await self.bot.get_shared_api_tokens("events")
        prebase_url = keys.get("prebase_url")
        token = keys.get("prebase_token")

        if prebase_url is None:
            return await ctx.reply("Prebase URL not found.")

        if token is None:
            return await ctx.reply("Prebase API token not found.")

        url = f"{prebase_url}/admin/actions/setredial"
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"SS14Token {token}"}
        data = {
            "Address": "",
            "Message": ""
        }

        response = requests.post(url, headers=headers, json=data)
        await ctx.reply("Clearing any events.")