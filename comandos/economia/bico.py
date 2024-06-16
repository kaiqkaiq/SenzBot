import discord
from discord import app_commands
from discord.ext import commands
import random
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


cooldowns = {}

coin = '<a:coin:1246247032734220318>'

class Bico(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="bico", description="💵 Economia | Faça um bico para ganhar dinheiro rapído")
    async def bico(self, sc: discord.Interaction ):
        user_id = str(sc.user.id)
        saldos = load_saldos()
        xps = load_xps()
        cooldown_time = 300

        if user_id in cooldowns and time.time() - cooldowns[user_id] < cooldown_time:
            await sc.response.send_message(f"⏰ | Você pode fazer um bico de novo em {int((cooldowns[user_id] + cooldown_time - time.time()) / 60)} minutos.", ephemeral=True)
            return
        
        bico = random.randint(25, 50)
        xpganho = random.randint(1, 3)
        if user_id not in xps:
            xps[user_id] = 0
        xps[user_id] += xpganho
        save_xps(xps)
        bicos = ['ajudou uma costureira',
                'trabalhou de ajudante de pedreiro',
                'trabalhou de Uber',
                'vendeu pastel na feira',
                'vendeu trufas no semáfaro',
                'gravou uma trend do TikTok',
                'ganhou um campeonato de algum jogo competitivo',
                'existiu,',
                'foi patrocinado misteriosamente',
                'lavou louça em um bar',
                'foi assasino de aluguel',
                'abriu comissões de desenho',
                'foi babá',
                'fez um bolo encomendado',
                'revendeu produtos na shopee',
                'passeou com o cachorro do vizinho']
        embed = discord.Embed(
                title=f'{coin} Bico', 
                description=f'''
Você {random.choice(bicos)} e ganhou `${bico}`
                ''', 
                color=discord.Color.yellow())
        embed.set_footer(text=f'+ {xpganho} XP')  
        
        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        saldos[user_id][0] += bico
        save_saldos(saldos)  
        await sc.response.send_message(embed=embed)
        cooldowns[user_id] = time.time()

    

async def setup(bot):
    await bot.add_cog(Bico(bot))