from ralsei.core.modules import fetch_modules
from discord.ext import commands
from importlib import reload

import discord


class Cog(commands.Cog):
    user_config = None
    server_config = None


class Modules:
    """
    Modules dynamo, manages all loaded "modules" which are essentially cogs installed by default to the bot
    """
    class ModulesCog(Cog, name="Modules Manager", command_attrs={"hidden": True}):
        """
        Owner only hidden cog, manages the modules loaded across all shards.
        """
        def __init__(self, bot, modules_dynamo):
            """
            Owner only hidden cog, manages the modules loaded across all shards.

            :param bot:
            :param modules_dynamo:
            """
            self.bot = bot
            self.dynamo = modules_dynamo

        @commands.is_owner()
        @commands.group(invoke_without_command=True, aliases=["mod"])
        async def modules(self, ctx):
            """
            Main command for managing modules.
            If used without an applicable subcommand, outputs the modules loaded

            :param ctx:
            :return loaded modules:
            """
            await ctx.send(embed=self.dynamo.get_modules())

        @modules.command(aliases=["+", "add"])
        async def load(self, ctx, module):
            """
            Subcommand of modules, loads module name `module` from the modules folder.

            :param ctx:
            :param module:
            :return status of module:
            """
            await ctx.send(embed=discord.Embed(title="Loaded Module",
                                               description=self.dynamo.load_module(
                                                   module,
                                                   __import__(f"ralsei.core.modules.{module}", fromlist=[module])
                                               )))

        @modules.command(aliases=["-", "del", "remove"])
        async def unload(self, ctx, module):
            """
            Subcommand of modules, unloads module name `module` from loaded modules

            :param ctx:
            :param module:
            :return status of module:
            """
            await ctx.send(embed=discord.Embed(title="Unloaded Module",
                                               description=self.dynamo.unload_module(
                                                   module
                                               )))

        @modules.command(aliases=["|", "rel"])
        async def reload(self, ctx, module):
            """
            Subcommand of modules, reloads module name `module` from loaded modules

            :param ctx:
            :param module:
            :return status of module:
            """
            await ctx.send(embed=discord.Embed(title="Reloaded Module",
                                               description=self.dynamo.reload_module(
                                                   module
                                               )))

    def __init__(self, bot):
        """
        Modules dynamo which manages all loaded "modules" for the bot
        Also adds the cog for managing loaded modules.

        :param bot:
        """

        self.bot = bot
        module_dict = fetch_modules()
        self.bot.add_cog(self.ModulesCog(self.bot, self))
        self.modules = {}

        for name, module in module_dict.items():
            print(self.load_module(name, module))

    def get_modules(self, raw=False):
        """
        Retrieve modules and return an embed for use with discord output.
        if raw=True, returns joined list
        :param raw:
        :return:
        """
        modules = "`\n`".join(self.modules.keys())
        embed = discord.Embed(title="Modules",
                              description=f"There are `{str(len(self.modules.keys()))}` loaded modules")
        if len(self.modules.keys()) > 0:
            embed.add_field(name="Loaded Modules:",
                            value=f"`{modules}`")
        return self.modules.keys() if raw else embed

    def load_module(self, name, module):
        if name not in self.modules.keys():
            try:
                reload(module)
                module.setup(self.bot)
                self.modules[name] = module
                return f"Succeeded in loading module {name} ({module})"
            except Exception as e:
                return e
        else:
            return f"Could not load module {name}: A module with that name already exists"

    def unload_module(self, name):
        if name in self.modules.keys():
            self.modules.pop(name).teardown(self.bot)
            return f"Succeeded in unloading module {name}"
        else:
            return f"Could not unload module {name}: No module with that name exists"

    def reload_module(self, name):
        if name in self.modules.keys():
            try:
                module = self.modules.pop(name)
                module.teardown(self.bot)
                reload(module)
                module.setup(self.bot)
                self.modules[name] = module
                return "Succeeded"
            except Exception as e:
                return e
        else:
            return "Could not unload module: No module with that name exists"
