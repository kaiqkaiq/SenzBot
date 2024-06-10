import discord
from discord import app_commands
from discord.ext import commands
import json

#* Userbadges
def load_userbadges():
    try:
        with open("./dados/userbadges.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_userbadges(userbadges):
    with open("./dados/fama.json", "w") as f:
        json.dump(userbadges, f, indent=4)

#* Badges
def load_badges():
    try:
        with open("./dados/badges.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


class allbadges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def badges(self, ctx:commands.Context):
        badges = load_badges()
        embed = discord.Embed(title='📌 Todas as badges', color=discord.Color.dark_red())
        for badge in badges:
            embed.add_field(name='', value=f'`ID: {badge}` **{badges[badge]}**', inline=False)
        await ctx.send(embed=embed)
    

async def setup(bot):
    await bot.add_cog(allbadges(bot))