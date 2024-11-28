from .ahelp_replies import AHelpReplies

async def setup(bot):
    await bot.add_cog(AHelpReplies(bot))