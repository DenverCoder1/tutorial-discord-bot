from nextcord.ext import commands
from .puzzle_view import NPuzzleView


class NPuzzleCog(commands.Cog, name="N-Puzzle"):
    """Play the sliding tile puzzle with buttons"""

    COG_EMOJI = "🧩"

    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.command()
    async def npuzzle(self, ctx: commands.Context, size: int = 4):
        """
        Starts a n-puzzle game, optionally with a given size (2-5).
        
        Example:
        ```
        ?npuzzle - starts a 4x4 puzzle
        ?npuzzle 3 - starts a 3x3 puzzle
        ```
        The goal is to get the numbers in order 1-n with the empty tile in the top left corner.
        """
        if not (2 <= size <= 5):
            await ctx.send('Size must be between 2 and 5.')
        await ctx.send('Click a tile adjacent to the empty tile to move it.', view=NPuzzleView(size))


def setup(bot: commands.Bot):
    bot.add_cog(NPuzzleCog(bot))
