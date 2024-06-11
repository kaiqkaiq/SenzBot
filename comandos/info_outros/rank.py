import discord
from discord import app_commands
from discord.ext import commands
import json

#* XP
def load_xps():
    try:
        with open('./dados/xp.json', "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_xps(xps):
    with open('./dados/xp.json', "w") as f:
        json.dump(xps, f, indent=4)

#* Famas
def load_famas():
    try:
        with open("./dados/fama.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_famas(famas):
    with open("./dados/fama.json", "w") as f:
        json.dump(famas, f, indent=4)

xpemoji = '<a:xp:1246253262533955655>'
famaemoji = '<a:rainbowfire:1246250924486426634>'

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='rank', description='🚬 Outros | Veja o rank de Fama ou XP')
    @app_commands.describe(categoria='Qual categoria?')
    @app_commands.choices(categoria=[
        app_commands.Choice(name='RankXP', value=2),
        app_commands.Choice(name='RankFAMA', value=1),
    ])
    async def rank(self, sc: discord.Interaction, categoria: app_commands.Choice[int]):
        if categoria.value == 1:
            global famas
            famas = load_famas()
            rank = sorted(famas.items(), key=lambda item: item, reverse=True)
        else:
            global xps
            xps = load_xps()
            rank = sorted(xps.items(), key=lambda item: item[1], reverse=True)
        if categoria.value == 1:
            emj = famaemoji
            c = '#FF00F7'
            rk = 'FAMA'
        else:
            emj = xpemoji
            c = '#E67E22'
            rk = 'XP'

        embed = discord.Embed(title=f'🏆 Rank de {rk}', color=discord.Color.from_str(c))

        for i, (user, value) in enumerate(rank[:10], start=1):
            userrank = await self.bot.fetch_user(user)
            embed.add_field(
                name='',
                value=f"🏅`#{i}` - {emj}`{value}` {userrank.display_name}",
                inline=False
            )
        
        await sc.response.send_message(embed=embed)

    

async def setup(bot):
    await bot.add_cog(Rank(bot))