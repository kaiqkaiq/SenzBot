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

tadapurple = '<a:tadapurple:1246250926445170751>'

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="daily", description="💵 Economia | Resgate seu prêmio diário")
    async def daily(self, sc: discord.Interaction):
        saldos = load_saldos()
        global xps
        xps = load_xps()
        user_id = str(sc.user.id)
        cooldown_time = 86400  #24h

        if user_id in cooldowns and time.time() - cooldowns[user_id] < cooldown_time:
            await sc.response.send_message(f"⏰ | Você já resgatou seu prêmio diário hoje, tente novamente em {int((cooldowns[user_id] + cooldown_time - time.time()) / 3600)} horas.", ephemeral=True)
            return
        
        daily = random.randint(900, 1850)
        xpganho = random.randint(10, 16)
        if user_id not in xps:
            xps[user_id] = 0
        xps[user_id] += xpganho
        save_xps(xps)
        embed = discord.Embed(
                title=f'{tadapurple} Prêmio Diário', 
                description=f'''
Você resgatou seu prêmio diário e ganhou `${daily}`
                ''', 
                color=discord.Color.from_str('#BC00FF'))  
        embed.set_footer(text=f'+ {xpganho} XP')

        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        saldos[user_id][0] += daily
        save_saldos(saldos)  
        await sc.response.send_message(embed=embed)
        cooldowns[user_id] = time.time()

    

async def setup(bot):
    await bot.add_cog(Daily(bot))