from .prebase_redial import prebase_redial

async def setup(bot):
    await bot.add_cog(prebase_redial(bot))