from nextcord.ext import commands
import random

class Random(commands.Cog, name="Random"):
    """Returns random results"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str):
        """Rolls a given amount of dice in the form _d_
        
        Example: ?roll 2d20
        """
        try:
            rolls = ""
            total = 0
            amount, die = dice.split("d")
            for _ in range(int(amount)):
                roll = random.randint(1, int(die))
                total += roll
                rolls += f"{roll} "
            await ctx.send(f"Rolls: {rolls}\nSum: {total}")
        except ValueError:
            await ctx.send("Dice must be in the format \_d\_ (example: 2d6)")

    @commands.command()
    async def choose(self, ctx: commands.Context, *args):
        """Chooses a random item from a list
        
        Example: ?choose "First Option" "Second Option" "Third Option"
        """
        try:
            choice = random.choice(args)
            await ctx.send(choice)
        except IndexError:
            await ctx.send("You must specify at least one argument.")

def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))