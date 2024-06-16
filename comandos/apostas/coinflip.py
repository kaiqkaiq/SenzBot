import discord
from discord import app_commands
from discord.ext import commands
import random
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





class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="coinflip", description="🎰 Apostas | Jogue cara ou coroa")
    @app_commands.describe(valor="O valor a ser apostado", escolha="Sua aposta",)
    @app_commands.choices(escolha=[
        app_commands.Choice(name='Cara', value='cara'),
        app_commands.Choice(name='Coroa', value='coroa'),
    ])
    async def coinflip(self, sc: discord.Interaction, valor: int, escolha: app_commands.Choice[str]):
        saldos = load_saldos()
        xps = load_xps()
        user_id = str(sc.user.id)
        
        if user_id not in xps:
            xps[user_id] = 0
        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        if xps[user_id] < 15:
            await sc.response.send_message(f'❗ | Você precisa de pelo menos `15` XP para apostar', ephemeral=True)
            return
        if saldos[user_id][0] < valor:
            await sc.response.send_message(f'❗ | Você não tem `${valor}`, pobre', ephemeral=True)
            return
        if valor <= 3:
            await sc.response.send_message(f'❗ | O valor precisa ser maior que três', ephemeral=True)
            return

        xpganho = random.randint(5, 15)
        result = random.choice(['cara', 'coroa'])
        if result == escolha.value:
            xps[user_id] += xpganho
            save_xps(xps)
            saldos[user_id][0] += int(valor*0.7)
            save_saldos(saldos)  

            embed = discord.Embed(
                    title='🪙 Cara ou coroa', 
                    description=f'''
*Você apostou `${valor}`, escolheu {escolha.value} e jogou a moeda...*

Caiu **{result}**! você ganhou `${int(valor*0.7)}`
                    ''', 
                    color=0x25c004) 
            embed.set_footer(text=f'+ {xpganho} XP')
            await sc.response.send_message(embed=embed)
        else:
            xps[user_id] -= int(xpganho / 1.5)
            save_xps(xps)
            saldos[user_id][0] -= valor
            save_saldos(saldos)  

            embed = discord.Embed(
                    title='🪙 Cara ou coroa', 
                    description=f'''
*Você apostou `${valor}`, escolheu {escolha.value} e jogou a moeda...*

Caiu **{result}**! mais sorte na próxima vez
                    ''', 
                    color=discord.Color.red())  
            embed.set_footer(text=f'- {xpganho} XP')
            await sc.response.send_message(embed=embed)
            

    

    

async def setup(bot):
    await bot.add_cog(Coinflip(bot))