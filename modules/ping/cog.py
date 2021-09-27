from nextcord.ext import commands

class Ping(commands.Cog, name="Ping"):
    """Receives ping commands"""

    COG_EMOJI = "🏓"

    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Checks for a response from the bot"""
        await ctx.send("Pong")

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))