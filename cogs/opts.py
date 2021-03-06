import discord
import config
import pymysql
from discord.ext import commands
from cogs.utils.db import *


def is_owner_or_manage(ctx):
    return ctx.author.id in config.owners or ctx.author.guild_permissions.manage_guild


class Settings:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner_or_manage)
    async def prefix(self, ctx, prefix: str = None):
        """Change the guild prefix.
        Note: to use this command, you must have the `MANAGE_GUILD` permission. If you wish to have a prefix with spaces, surround it in "quotes" """
        if not prefix:
            try:
                return await ctx.send(f'My prefix here is `{self.bot.prefixes[str(ctx.guild.id)]}`. You can change that with `{ctx.prefix}prefix <prefix>`')
            except KeyError:
                return await ctx.send(f'My prefix here is `{config.prefix[0]}`. You can change that with `{ctx.prefix}prefix <prefix>`')
        db = pymysql.connect(config.db_ip, config.db_user, config.db_pass, config.db_name)
        cur = db.cursor()
        cur.execute(
            f"""INSERT INTO settings (guildid, prefix) VALUES ({ctx.guild.id}, "{prefix}") ON DUPLICATE KEY UPDATE prefix = "{prefix}";""")
        db.commit()
        db.close()
        self.bot.prefixes = get_all_prefixes()
        await ctx.send(f':ok_hand: Successfully set my prefix here to `{prefix}`')


def setup(bot):
    bot.add_cog(Settings(bot))
