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


creditcard = '<a:creditcard:1246251203080355840>'

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="ec-transferir", description="💵 Economia | Transfira dinheiro à alguém")
    @app_commands.describe(valor="O valor a ser depositado", usuario='O usuário a transferir')
    async def pay(self, sc: discord.Interaction, valor: int, usuario: discord.User):
        saldos = load_saldos()
        user_id = str(sc.user.id)
        mentioned_id = str(usuario.id)
        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        if mentioned_id not in saldos:
            saldos[mentioned_id] = [0, 0,]
        if usuario == sc.user:
            await sc.response.send_message(f'❗ | Você não pode transferir para você mesmo.', ephemeral=True)
            return      
        if usuario.bot:
            await sc.response.send_message(f'❗ | O usuário é um bot.', ephemeral=True)
            return
        if valor <= 0:
            await sc.response.send_message(f'❗ | O valor precisa ser maior que zero', ephemeral=True)
            return
        if saldos[user_id][0] < valor:
            await sc.response.send_message(f'❗ | Você não tem `{valor}` para fazer a transferência', ephemeral=True)
            return

        saldos[user_id][0] -= valor
        saldos[mentioned_id][0]  += valor
        save_saldos(saldos)  

        embed = discord.Embed(
                title=f'{creditcard} Transferência feita', 
                description=f'{sc.user.mention} transferiu `${valor}` para {usuario.mention}', 
                color=discord.Color.from_str('#BC00FF'))  
        await sc.response.send_message(content=f'{usuario.mention}', embed=embed)
    

async def setup(bot):
    await bot.add_cog(Pay(bot))