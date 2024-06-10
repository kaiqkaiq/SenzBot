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


class badges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='badges', description='🛹 Perfil | Veja as badges que você possui')
    async def badges(self, sc:discord.Interaction):
        user_id = str(sc.user.id)
        userbadges = load_userbadges()
        badges = load_badges()
        embed = discord.Embed(title='📌 Suas badges', color=discord.Color.dark_red())
        for badge in userbadges[user_id]:
            embed.add_field(name='', value=f'`ID: {badge}` **{badges[badge]}**', inline=False)
        embed.set_thumbnail(url=sc.user.avatar)
        await sc.response.send_message(embed=embed)
    

async def setup(bot):
    await bot.add_cog(badges(bot))