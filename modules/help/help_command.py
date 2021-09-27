import nextcord
from nextcord.ext import commands


class HelpDropdown(nextcord.ui.Select):
    def __init__(self, options: list[nextcord.SelectOption]):
        super().__init__(placeholder='Choose a category...',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        view: SelectHelpCommand = self.view
        assert view is not None
        embed = None
        # home page selected
        if self.values[0] == self.options[0].value:
            embed = await view._bot_help_embed(view.get_bot_mapping())
        # cog page selected
        else:
            embed = await view._cog_help_embed(view.context.bot.get_cog(self.values[0]))
        await interaction.response.edit_message(embed=embed)


class SelectHelpCommand(commands.MinimalHelpCommand, nextcord.ui.View):
    """Custom help command override using embeds"""

    def __init__(self):
        commands.MinimalHelpCommand.__init__(self)
        nextcord.ui.View.__init__(self, timeout=120.0)
        # attribute for storing response message
        self.response = None
    
    async def on_timeout(self):
        if isinstance(self.response, nextcord.Message):
            self.clear_items()
            await self.response.edit(view=self)

    async def _bot_help_embed(self, mapping: dict):
        select_options: list[nextcord.SelectOption] = []
        select_options.append(nextcord.SelectOption(emoji="🏠", label="Home", description="Return to home page"))
        embed = nextcord.Embed(title="Bot Commands")
        avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
        embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            label = "No Category" if cog is None else cog.qualified_name
            emoji = getattr(cog, 'COG_EMOJI', None)
            name = f"{emoji} {label}" if emoji else label
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered)
                description = cog.description if cog and cog.description else None
                if description:
                    value = f"{description}\n{value}"
                embed.add_field(name=name, value=value)
                # add cog to select options
                select_options.append(nextcord.SelectOption(
                    label=label, description=description,
                    emoji=getattr(cog, "COG_EMOJI", None)
                ))

        embed.set_footer(text=self.get_ending_note())

        # add help dropdown
        if not len(self.children):
            self.add_item(HelpDropdown(select_options))
        return embed

    async def _cog_help_embed(self, cog: commands.Cog):
        """
        Returns an embed for a cog
        """
        emoji = getattr(cog, 'COG_EMOJI', None)
        name = f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name
        embed = nextcord.Embed(title=f"{name} Commands")
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=f"`{self.context.clean_prefix}{self.get_command_signature(command)}`",
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        return embed

    async def _command_help_embed(self, command: commands.Command):
        """
        Returns an embed for a command or command group
        """
        emoji = getattr(command.cog, "COG_EMOJI", None)
        title = f"{emoji} {command.qualified_name}" if emoji else command.qualified_name
        embed = nextcord.Embed(title=title)
        if command.help:
            embed.description = command.help

        if isinstance(command, commands.Group):
            filtered = await self.filter_commands(command.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=f"`{self.context.clean_prefix}{self.get_command_signature(command)}`",
                    value=command.short_doc or "...",
                    inline=False,
                )

        embed.set_footer(text=self.get_ending_note())
        return embed

    def get_ending_note(self):
        """Returns note to display at the bottom"""
        return f"Use {self.context.clean_prefix}{self.invoked_with} [command] for more info on a command."

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        self.response = await self.get_destination().send(embed=await self._bot_help_embed(mapping), view=self)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        await self.get_destination().send(embed=await self._cog_help_embed(cog))

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        await self.get_destination().send(embed=await self._command_help_embed(group))

    # Use the same function as group help for command help
    send_command_help = send_group_help
