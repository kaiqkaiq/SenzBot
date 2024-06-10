import discord
from discord import app_commands
from discord.ext import commands
import time
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

cooldowns = {}

class banco(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()


    @app_commands.command(name="depositar", description="💵 Economia | Deposite dinheiro no banco")
    @app_commands.describe(valor="O valor a ser depositado")
    async def deposit(self, sc: discord.Interaction, valor: int):
        saldos = load_saldos()
        user_id = str(sc.user.id)
        cooldown_time = 7 * 60

        if user_id in cooldowns and time.time() - cooldowns[user_id] < cooldown_time:
            await sc.response.send_message(f"⏰ | Deposite de novo em {int((cooldowns[user_id] + cooldown_time - time.time()) / 60)} minutos.", ephemeral=True)
            return
        if user_id not in saldos:
            saldos[user_id] = [0, 0,] 
        if saldos[user_id][0] < valor:
            await sc.response.send_message(f'❗ | Você não tem `${valor}`para depositar.', ephemeral=True)
            return
        if valor <= 0:
            await sc.response.send_message(f'❗ | O valor precisa ser maior que zero', ephemeral=True)
            return
        
        taxa = int((valor / 100) * 3)
        saldos[user_id][0] -= valor
        saldos[user_id][1]  += valor - taxa
        save_saldos(saldos)  

        embed = discord.Embed(
                title='🏦 Depósitado', 
                description=f'''
Você depositou `${valor - taxa}` em seu banco
*Taxa: `${taxa}` (3% de `${valor}`)*
                ''', 
                color=discord.Color.og_blurple())  
        await sc.response.send_message(embed=embed)            

        cooldowns[user_id] = time.time()


    @app_commands.command(name="sacar", description="💵 Economia | saque dinheiro do banco")
    @app_commands.describe(valor="O valor a ser retirado")
    async def saque(self, sc: discord.Interaction, valor: int):
        saldos = load_saldos()
        user_id = str(sc.user.id)

        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        if saldos[user_id][1] < valor:
            await sc.response.send_message(f'❗ | Você não tem `${valor}` para retirar.', ephemeral=True)
            return
        if valor <= 0:
            await sc.response.send_message(f'❗ | O valor precisa ser maior que zero', ephemeral=True)
            return
       
        saldos[user_id][1] -= valor
        saldos[user_id][0]  += valor
        save_saldos(saldos)  

        embed = discord.Embed(
                title='🏦 Retirado', 
                description=f'Você retirou `${valor}` de seu banco.', 
                color=discord.Color.og_blurple())  
        await sc.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(banco(bot))