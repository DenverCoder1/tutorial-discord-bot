import os
from dotenv.main import load_dotenv
from discord.ext import commands

def main():
    client = commands.Bot(command_prefix="?")

    load_dotenv()

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")

    # @client.event
    # async def on_message(ctx):
    #     if (ctx.content.startswith("Hello")):
    #         await ctx.channel.send(f"Hi {ctx.author.mention}!")

    @client.command()
    async def ping(ctx):
        """Checks for a response from the bot"""
        await ctx.send("Pong")

    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()