from discord.ext import commands
import discord
from .modules import Cog


class Extensions:
    """
    Ralsei dynamo for managing extensions
    """
    class ExtensionsCog(Cog, name="Extensions Manager", command_attrs={"hidden": True}):
        """
        Cog connection for management of extensions through the bot itself
        """
        def __init__(self, bot, extensions_dynamo):
            """
            Cog connection for management of extensions through the bot itself
            """
            self.bot = bot
            self.dynamo = extensions_dynamo

        @commands.is_owner()
        @commands.group(invoke_without_command=True, aliases=["ext"])
        async def extensions(self, ctx):
            """
            Base command for managing extensions. If run without a subcommand, lists loaded extensions

            :param ctx:
            :return loaded extension:
            """

            await ctx.send(embed=self.dynamo.get_extensions())

        @extensions.command(aliases=["+", "add"])
        async def load(self, ctx, extension):
            """
            Subcommand of extensions, loads extension from dot notated path `extension`

            :param ctx:
            :param extension:
            :return status of extension:
            """
            await ctx.send(embed=discord.Embed(title="Loaded Extension",
                                               description=self.dynamo.load_extension(extension)))

        @extensions.command(aliases=["-", "del", "remove"])
        async def unload(self, ctx, extension):
            """
            Subcommand of extensions, unloads extension from dot notated path `extension`

            :param ctx:
            :param extension:
            :return status of extension:
            """
            await ctx.send(embed=discord.Embed(title="Unloaded Extension",
                                               description=self.dynamo.unload_extension(extension)))

        @extensions.command(aliases=["|", "rel"])
        async def reload(self, ctx, extension):
            """
            Subcommand of extensions, reloads extension from dot notated path `extension`

            :param ctx:
            :param extension:
            :return status of extension:
            """
            await ctx.send(embed=discord.Embed(title="Reloaded Extension",
                                               description=self.dynamo.reload_extension(extension)))

        @extensions.command(aliases=["||"])
        async def reload_all(self, ctx, extension):
            """
            Subcommand of extensions, reloads all loaded extensions

            :param ctx:
            :param extension:
            :return status of extension:
            """
            await ctx.send(embed=self.dynamo.reload_all_extensions(extension))

    def get_extensions(self, raw=False):
        """
        Gathers extensions and returns a string of extensions

        :return extensions string:
        """
        extensions = "`\n`".join(self.extensions)
        embed = discord.Embed(title="Extensions",
                              description=f"There are `{str(len(self.extensions))}` loaded extensions")
        if len(self.extensions) > 0:
            embed.add_field(name="Loaded Extensions:", value=f"`{extensions}`")

        return self.extensions if raw else embed

    def load_extension(self, extension):
        """
        Loads extension `extension` and returns status

        :param extension:
        :return status:
        """
        try:
            self.bot.load_extension(extension)
            return f"Extension {extension} loaded"
        except Exception as e:
            return e

    def unload_extension(self, extension):
        """
        Unloads extension `extension` and returns status

        :param extension:
        :return status:
        """
        try:
            if extension in self.extensions:
                self.bot.unload_extension(extension)
                return f"Extension {extension} unloaded"
            else:
                return f"Extension {extension} not loaded"
        except Exception as e:
            return e

    def reload_extension(self, extension):
        """
        Reloads extension `extension` and returns status

        :param extension:
        :return status:
        """
        try:
            if extension in self.extensions:
                self.unload_extension(extension)
                return self.load_extension(extension)
            else:
                return f"Extension {extension} not loaded"
        except Exception as e:
            return e

    def reload_all(self):
        """
        Reloads all extensions and returns list of statuses for reloading

        :return status list:
        """
        output = []
        try:
            if len(self.extensions) > 0:
                for extension in self.extensions:
                    output.append(self.reload_extension(extension))

                successes = len(output)-len([i for i in output if not i.startswith("Extension")
                                             and not i.endswith("not loaded")])

                embed = discord.Embed(title="Reloaded Extensions",
                                      description=f"`{str(successes)}` succeeded\n`{str(len(output)-successes)}` failed"
                                      )

                out = "`\n`".join(output)
                embed.add_field(name="Output:", value=f"`{out}`")

                return embed
            else:
                return discord.Embed(title="No Extensions Loaded",
                                     description="Could not reload extensions, as there are none.")
        except Exception as e:
            return e

    def __init__(self, bot):
        """
        sets up extension dynamo
        Adds respective cog to bot

        :param bot:
        """
        self.bot = bot
        self.extensions = []
        self.bot.add_cog(self.ExtensionsCog(bot, self))
