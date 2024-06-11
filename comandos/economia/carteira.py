import discord
from discord import app_commands
from discord.ext import commands
import json

#* SALDOS
def load_saldos():
    try:
        with open("./dados/saldos.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_saldos(saldos):
    with open("./dados/saldos.json", "w") as f:
        json.dump(saldos, f, indent=4)


carteiraemoji = '<:carteira:1246247426449473546>'


class Carteira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="carteira", description="💵 Economia | Veja seu saldo")
    async def carteira(self, sc: discord.Interaction):
        saldos = load_saldos()

        user_id = str(sc.user.id)
        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
            save_saldos(saldos)
        embed = discord.Embed(
                title=f'{carteiraemoji} Saldo', 
                description=f'''
>>> Carteira: `${saldos[user_id][0]}`
Banco: `${saldos[user_id][1]}`
                ''', 
                color=discord.Color.blue())
        await sc.response.send_message(embed=embed)

    

    

async def setup(bot):
    await bot.add_cog(Carteira(bot))