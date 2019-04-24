from discord.ext import commands
import discord

import ralsei.core.dynamos as dynamos


class Ralsei(commands.Bot):
    """
    The Ralsei bot itself
    """
    class Base(dynamos.modules.Cog, name="Base Commands"):
        def __init__(self, bot):
            """
            Internal cog containing the base commands for Ralsei.

            :param bot:
            """
            self.bot = bot

        @commands.is_owner()
        @commands.command()
        async def shutdown(self, ctx):
            await ctx.send("Goodbye!")
            await self.bot.close()

        @commands.is_owner()
        @commands.command()
        async def prefix(self, ctx, prefix: str):
            if type(ctx.channel) is not discord.DMChannel:

                await ctx.send(f"Changed {ctx.guild}'s prefix from "
                               f"{self.bot.config[str(ctx.guild.id)]['prefix']} to {prefix}")
                self.bot.config[str(ctx.guild.id)] = {"prefix": prefix}
            else:
                try:
                    await ctx.send(f"Sorry, but user specific prefixes are not yet supported.")
                except Exception as e:
                    print(f"{ctx.author}: {e}")

    async def on_ready(self):
        print(f"{self.config['Ralsei']['name']} Ready")

    async def on_command_error(self, context, exception):
        print(context.command)
        print(context.cog)
        print(exception)
        print(type(exception))
        try:
            await context.send(str(exception))
        except Exception as e:
            print(e)
            pass

    def add_cog(self, cog: dynamos.modules.Cog):
        """
        Registers a cog to the Ralsei bot.

        Also registers the cog with all applicable dynamos.

        :param cog:
        """
        self.dynamos["storage"].register_config(cog)
        self.config.register_cog(cog)
        super().add_cog(cog)

    @staticmethod
    def _dynamic_prefix(bot, message) -> str:
        """
        Dynamically returns a prefix (used with the bot itself)

        :param bot:
        :param message:
        :return prefix:
        """
        if type(message.channel) is not discord.DMChannel:
            return bot.config[str(message.guild.id)]["prefix"]
        else:
            return bot.config["Ralsei"]["command_prefix"]

    def __init__(self, config_file="RalseiConfig.ini"):
        self.config, self.dynamos = dynamos.Config(config_file), {}

        self.token = self.config["Ralsei"]["token"]

        if self.token is "":
            raise Warning("Token not set. Please set a token.")

        super().__init__(command_prefix=self._dynamic_prefix,
                         case_insensitive=self.config["Ralsei"]["case_insensitive"],
                         owner_id=int(self.config["Ralsei"]["owner_id"]) if
                         self.config["Ralsei"]["owner_id"] is not "" else None)

        if self.config["Ralsei"]["presence"] is not "":
            self.activity = discord.Game(name=self.config["Ralsei"]["presence"])

        self.dynamos["storage"] = dynamos.Storage(self)
        self.dynamos["extensions"] = dynamos.Extensions(self)
        self.dynamos["modules"] = dynamos.Modules(self)

        self.add_cog(self.Base(self))

    def start_bot(self, token=None):
        token = token if token is not None else self.token

        try:
            self.run(token)
        except Exception as e:
            print(e)
            raise SystemExit
