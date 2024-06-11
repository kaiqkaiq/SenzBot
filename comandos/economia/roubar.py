import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import time

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


moneybag = '<a:moneybag:1247728074632724480>'
xmark = '<a:xmark:1247729020414464020>'
vmark = '<a:vmark:1247729112907386950>'
xpemoji = '<a:xp:1246253262533955655>'

cooldownsx = {}
cooldownsy = {}

class Roubar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="roubar", description="💵 Economia | Roube dinheiro (e XP) de alguém")
    @app_commands.describe(usuario='O usuário que você vai (tentar) roubar')
    async def Roubar(self, sc: discord.Interaction, usuario: discord.User):
        saldos = load_saldos()
        xps = load_xps()
        user_id = str(sc.user.id)
        mentioned_id = str(usuario.id)

        cooldownx_time = 5400 #1h 30m, Cooldown se der certo
        cooldowny_time = 600 #10m, Cooldown se der errado

        if user_id in cooldownsx and time.time() - cooldownsx[user_id] < cooldownx_time:
            await sc.response.send_message(f"⏰ | Tente roubar alguém novamente em {int((cooldownsx[user_id] + cooldownx_time - time.time()) / 60)} minutos.", ephemeral=True)
            return
        if user_id in cooldownsx and time.time() - cooldownsy[user_id] < cooldowny_time:
            await sc.response.send_message(f"⏰ | Tente roubar alguém novamente em {int((cooldownsy[user_id] + cooldowny_time - time.time()) / 60)} minutos.", ephemeral=True)
            return

        if user_id not in saldos:
            saldos[user_id] = [0, 0,]
        if mentioned_id not in saldos:
            saldos[mentioned_id] = [0, 0,]
        if user_id not in xps:
            xps[user_id] = 0
        if mentioned_id not in xps:
            xps[mentioned_id] = 0
        
        if usuario == sc.user:
            await sc.response.send_message(f'❗ | Oxi? Você não pode roubar você mesmo', ephemeral=True)
            return      
        if usuario.bot:
            await sc.response.send_message(f'❗ | O usuário é um bot', ephemeral=True)
            return
        if saldos[mentioned_id][0] < 250:
            await sc.response.send_message(f'❗ | O usuário é pobre demais, nem tem o que roubar (Ou foi inteligente e depositou o que tinha)', ephemeral=True)
            return
        if xps[mentioned_id] < 10:
            await sc.response.send_message(f'❗ | O usuário precisa de pelo menos dez de XP (Pô, deve ser iniciante, maldade)', ephemeral=True)
            return
        if xps[user_id] < 10:
            await sc.response.send_message(f'❗ | Você precisa de pelo menos dez de XP', ephemeral=True)
            return
        
        xpg = random.randint(6, 10)
        rbd = random.randint(150, 250)

        if random.randint(1, 2) == 1:

            saldos[user_id][0] += rbd
            saldos[mentioned_id][0]  -= rbd
            xps[user_id] += xpg
            xps[mentioned_id]  -= xpg
            save_saldos(saldos)
            save_xps(xps)  
            r = random.choice([
                'furtou',
                'assaltou',
                'inavdiu a casa e pegou',
                'pegou e saiu correndo com',
                'deu um golpe e levou'
            ])
            embed = discord.Embed(
                    title=f'{moneybag} Roubo', 
                    description=f'''
**{vmark} {sc.user.mention} {r} `${rbd}` de {usuario.mention}**
>>> - {xpemoji}`{xpg}` XP para {usuario.display_name}
+ {xpemoji}`{xpg}` XP para {sc.user.display_name}
''', 
                    color=discord.Color.yellow())  
            await sc.response.send_message(content=f'{usuario.mention}', embed=embed)
            cooldownsx[user_id] = time.time()
        else:
            xps[user_id] -= xpg
            save_xps(xps)  
            embed = discord.Embed(
                    title=f'{moneybag} Roubo', 
                    description=f'{xmark} {sc.user.mention} não conseguiu roubar {usuario.mention}', 
                    color=discord.Color.red())
            embed.set_footer(text=f'- {xpg} XP')
            
            cooldownsy[user_id] = time.time()
            await sc.response.send_message(content=f'{usuario.mention}', embed=embed)
    

async def setup(bot):
    await bot.add_cog(Roubar(bot))