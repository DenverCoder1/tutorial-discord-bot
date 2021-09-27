from nextcord.ext import commands

from .help_command import SelectHelpCommand


class HelpCog(commands.Cog, name="Help"):
    """Shows help info for commands and cogs"""

    COG_EMOJI = "❔"

    def __init__(self, bot: commands.Bot):
        self._original_help_command = bot.help_command
        self._bot = bot
        self._bot.help_command = SelectHelpCommand()
        self._bot.help_command.cog = self

    def cog_unload(self):
        self._bot.help_command = self._original_help_command


# setup functions for bot
def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))
