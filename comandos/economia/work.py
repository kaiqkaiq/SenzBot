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
xpemoji = '<a:xp:1246253262533955655>'

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="trabalhar", description="💵 Economia | Trabalhe e ganhe dinheiro")
    async def work(self, sc: discord.Interaction):
        saldos = load_saldos()
        xps = load_xps()
        user_id = str(sc.user.id)
        cooldown_time = 1200 

        if user_id in cooldowns and time.time() - cooldowns[user_id] < cooldown_time:
            await sc.response.send_message(f"⏰ | Você pode trabalhar de novo em {int((cooldowns[user_id] + cooldown_time - time.time()) / 60)} minutos.", ephemeral=True)
            return
        
        work = random.randint(150, 350)
        xpganho = random.randint(3, 7)
        if user_id not in xps:
            xps[user_id] = 0
        xps[user_id] += xpganho
        save_xps(xps)

        embed = discord.Embed(
                title=f'{coin} Trabalho', 
                description=f'''
Você trabalhou e ganhou `${work}`
                ''', 
                color=discord.Color.yellow()) 
        embed.set_footer(text=f'+ {xpganho} XP!')

        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        saldos[user_id][0] += work
        save_saldos(saldos)  
        await sc.response.send_message(embed=embed)
        cooldowns[user_id] = time.time()

    

async def setup(bot):
    await bot.add_cog(Work(bot))