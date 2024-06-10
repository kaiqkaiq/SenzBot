import discord
from discord import app_commands
from discord.ext import commands
import time
import json
import random

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


cooldowns = {}
vezescld = {}

xpemoji = '<a:xp:1246253262533955655>'
famaemoji ='<a:rainbowfire:1246250924486426634>'

class Darfama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()


    @app_commands.command(name="fama", description="🛹 Perfil | Dê fama à alguém")
    @app_commands.describe(usuario="Para quem você vai dar?")
    async def fama(self, sc: discord.Interaction, usuario: discord.User):
        xps = load_xps()
        famas = load_famas()
        user_id = str(usuario.id)
        autor_id = str(sc.user.id)
        cooldown_time = 86400

        if autor_id in cooldowns and time.time() - cooldowns[autor_id] < cooldown_time:
            await sc.response.send_message(f"⏰ | Você já deu demais hoje, espere {int((cooldowns[autor_id] + cooldown_time - time.time()) / 3600)} horas para dar mais", ephemeral=True)
            return
        if usuario == sc.user:
            await sc.response.send_message(f'❗ | Você não pode dar pra você mesmo (Isso fica estranho sem contexto)', ephemeral=True)
            return
        if usuario == self.bot.user:
            await sc.response.send_message(f'❗ | Obrigado, mas não quero nada não, pode dar para outra pessoa', ephemeral=True)
            return
        if usuario.bot:
            await sc.response.send_message(f"❗ | Bots não precisam de fama, dê para alguém real", ephemeral=True)
            return
        
        if user_id not in xps:
            xps[user_id] = 0
            save_xps(xps)
        if user_id not in famas:
            famas[user_id] = 0
            save_famas(famas)
        if autor_id not in xps:
            xps[autor_id] = [0]
            save_xps(xps)
        
        xpganho = random.randint(3, 7)
        famaganha = random.randint(1, 3)
        famas[user_id][0] += famaganha
        save_famas(famas)
        xps[user_id]  += xpganho
        xps[autor_id]  += xpganho 
        save_xps(xps) 

        embed = discord.Embed(
                title=f'{famaemoji} Fama', 
                description=f'''
{sc.user.mention} deu fama para {usuario.mention}
>>> **+ {famaemoji}`{famaganha}` FAMA** para {usuario.display_name}
**+ {xpemoji}`{xpganho}` XP** para {usuario.display_name}
**+ {xpemoji}`{xpganho}` XP** para {sc.user.display_name}
''', 
                color=discord.Color.from_str('#FF00F7'))  
        await sc.response.send_message(content=f'{usuario.mention}', embed=embed)            

        if autor_id not in vezescld:
            vezescld[autor_id] = 0
        vezescld[autor_id] += 1
        if vezescld[autor_id] == 5:
            cooldowns[autor_id] = time.time()
            vezescld[autor_id] = 0


    

async def setup(bot):
    await bot.add_cog(Darfama(bot))