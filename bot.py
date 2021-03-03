import os
from dotenv import load_dotenv
from discord.ext import commands

def main():
    client = commands.Bot(command_prefix="?")

    load_dotenv()

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")

    # @client.event
    # async def on_message(message):
    #     if (message.content.startswith("Hello")):
    #         await message.channel.send(f"Hi {message.author.mention}!")

    @client.command()
    async def ping(ctx):
        """Checks for a response from the bot"""
        await ctx.send("Pong")

    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()