from typing import Iterable, Optional, Set
import nextcord
from nextcord.ext import commands


class HelpDropdown(nextcord.ui.Select):
    def __init__(self, help_command: "SelectHelpCommand", options: list[nextcord.SelectOption]):
        super().__init__(placeholder='Choose a category...',
                         min_values=1, max_values=1, options=options)
        self._help_command = help_command

    async def callback(self, interaction: nextcord.Interaction):
        embed = (
            # home page selected
            await self._help_command._bot_help_embed(self._help_command.get_bot_mapping())
            if self.values[0] == self.options[0].value
            # cog page selected
            else await self._help_command._cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
        )
        await interaction.response.edit_message(embed=embed)


class HelpView(nextcord.ui.View):
    def __init__(self, help_command: "SelectHelpCommand", options: list[nextcord.SelectOption], *, timeout: Optional[float] = 120.0):
        super().__init__(timeout=timeout)
        self._help_command = help_command
        self.add_item(HelpDropdown(help_command=help_command, options=options))

    async def on_timeout(self):
        # remove dropdown from message on timeout
        self.clear_items()
        await self._help_command.response.edit(view=self)


class SelectHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    async def _cog_select_options(self) -> list[nextcord.SelectOption]:
        options: list[nextcord.SelectOption] = []
        # add the home option
        options.append(nextcord.SelectOption(
            emoji="🏠", label="Home", description="Return to home page"
        ))
        # add options for each cog with available commands
        for cog, commands in self.get_bot_mapping().items():
            if not await self.filter_commands(commands, sort=True):
                continue
            # add cog to select options
            options.append(nextcord.SelectOption(
                label="No Category" if cog is None else cog.qualified_name,
                description=cog.description if cog and cog.description else None,
                emoji=getattr(cog, 'COG_EMOJI', None),
            ))
        return options

    async def _help_embed(
        self, title: str, description: Optional[str] = None,
        command_set: Optional[Set[commands.Command]] = None,
        mapping: Optional[dict] = None, set_author: bool = False
    ):
        """
        Returns an embed for a command or set of commands, for example in a group or cog

        Arguments
        """
        embed = nextcord.Embed(title=title)
        # set description of bot, cog, or single command help
        if description:
            embed.description = description
        # set author to show bot info for bot help page
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name=self.context.bot.user.name,
                             icon_url=avatar.url)
        # show help for all commands in a set
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(
                    name=f"`{self.context.clean_prefix}{self.get_command_signature(command)}`",
                    value=command.short_doc or "...",
                    inline=False,
                )
        # show brief list of commands in each cog
        elif mapping:
            # add cogs with command names as fields
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = "No Category" if cog is None else cog.qualified_name
                emoji = getattr(cog, 'COG_EMOJI', None)
                cog_label = f"{emoji} {name}" if emoji else name
                # \u2002 = en space
                cmd_list = "\u2002".join(
                    f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
                )
                value = f"{cog.description}\n{cmd_list}" if cog and cog.description else cmd_list
                embed.add_field(name=cog_label, value=value)
        embed.set_footer(text=self.get_ending_note())
        return embed

    async def _bot_help_embed(self, mapping: dict):
        return await self._help_embed(
            title="Bot Commands",
            description=self.context.bot.description,
            mapping=mapping,
            set_author=True,
        )

    async def _cog_help_embed(self, cog: commands.Cog):
        """
        Returns an embed for a cog
        """
        emoji = getattr(cog, 'COG_EMOJI', None)
        name = f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name
        return await self._help_embed(
            title=f"{name} Commands",
            description=cog.description,
            command_set=cog.get_commands(),
        )

    async def _command_help_embed(self, command: commands.Command):
        """
        Returns an embed for a command or command group
        """
        emoji = getattr(command.cog, "COG_EMOJI", None)
        command_set = (
            command.commands
            if isinstance(command, commands.Group)
            else None
        )
        return await self._help_embed(
            title=f"{emoji} {command.qualified_name}" if emoji else command.qualified_name,
            description=command.help,
            command_set=command_set,
        )

    def get_ending_note(self):
        """Returns note to display at the bottom"""
        return f"Use {self.context.clean_prefix}{self.invoked_with} [command] for more info on a command."

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        options = await self._cog_select_options()
        self.response = await self.get_destination().send(embed=await self._bot_help_embed(mapping), view=HelpView(self, options))

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        await self.get_destination().send(embed=await self._cog_help_embed(cog))

    async def send_command_help(self, command: commands.Command):
        """implements help page for commands and command groups"""
        await self.get_destination().send(embed=await self._command_help_embed(command))

    # Use the same function as command help for group help
    send_group_help = send_command_help
