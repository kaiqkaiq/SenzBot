import discord
from discord import app_commands
from discord.ext import commands
import json
import random

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

class apostar(discord.ui.View):
    def __init__(self, valor, user_id):
        super().__init__(timeout=60)
        self.valor = valor
        self.user_id = user_id

    @discord.ui.button(label='Apostar!', style=discord.ButtonStyle.green, emoji='💸')
    async def botaoapostar(self, sc: discord.Interaction, botao: discord.ui.Button):
        if str(sc.user.id) != self.user_id:
            await sc.response.send_message("❗ | Não é você que vai apostar!", ephemeral=True)
            return
        
        saldos = load_saldos()
        xps = load_xps()
        
        if self.user_id not in xps:
            xps[self.user_id] = 0
        if self.user_id not in saldos:
            saldos[self.user_id] = [0, 0,]
        if xps[self.user_id] < 15:
            await sc.response.send_message(f'❗ | Você precisa de pelo menos `15` XP para apostar', ephemeral=True)
            return
        if saldos[self.user_id][0] < self.valor:
            await sc.response.send_message(f'❗ | Você não tem `${self.valor}`, pobre', ephemeral=True)
            return
        
        simbolos = ['🐀','🍌','🍒','🍓','🥝','💎']
        result = [random.choice(simbolos) for _ in range(3)]

# * TRÊS DIAMANTES
        if result[0] == '💎' and result[1] == '💎' and result[2] == '💎':
            xps[self.user_id] += random.randint(7, 12)
            save_xps(xps)
            saldos[self.user_id][0] += self.valor * 3 
            save_saldos(saldos)

            embed = discord.Embed(color=0x7bd4ff, title='🎰 Caça-níquel', description=
f'''
{sc.user.display_name} Puxou a alavanca

**Você conseguiu:**
**{' • '.join(result)}**

Parabéns! Você ganhou `${self.valor * 3}!`
''',)
            embed.set_footer(text=f'+ {random.randint(7, 12)} XP')
        
# * TRÊS RATOS
        elif result[0] == '🐀' and result[1] == '🐀' and result[2] == '🐀':
            xps[self.user_id] -= random.randint(7, 15)
            save_xps(xps)
            if saldos[self.user_id][0] < saldos[self.user_id] * 2.5:
                saldos[self.user_id][0] -= int(self.valor * 2.5)
                perdeu = int(self.valor * 2.5)
            else:
                saldos[self.user_id][0] -= self.valor
                perdeu = self.valor
            save_saldos(saldos)
            embed = discord.Embed(color=0x1e0303, title='🎰 Caça-níquel', description=
f'''
{sc.user.display_name} Puxou a alavanca

**Você conseguiu:**
**{' • '.join(result)}**

Mais sorte na próxima, Você perdeu `${perdeu}!`
''',)
            embed.set_footer(text=f'- {random.randint(7, 15)} XP')
        
# * COMBINAÇÃO TRÊS
        elif result[0] == result[1] == result[2]:
            xps[self.user_id] += random.randint(3, 8)
            save_xps(xps)
            saldos[self.user_id][0] += int(self.valor * 1.5)
            save_saldos(saldos)

            embed = discord.Embed(color=discord.Color.yellow(), title='🎰 Caça-níquel', description=
f'''
{sc.user.display_name} Puxou a alavanca

**Você conseguiu:**
**{' • '.join(result)}**

Parabéns! Você ganhou `${int(self.valor * 1.5)}!`
''',)
            embed.set_footer(text=f'+ {random.randint(3, 8)} XP')

# * COMBINAÇÃO DOIS
        elif result[0] == result[1] or result[0] == result[2] or result[1] == result[2]:
            xps[self.user_id] += random.randint(2, 5)
            save_xps(xps)
            saldos[self.user_id][0] += int(self.valor * 0.6)
            save_saldos(saldos)

            embed = discord.Embed(color=0x25c004, title='🎰 Caça-níquel', description=
f'''
{sc.user.display_name} Puxou a alavanca

**Você conseguiu:**
**{' • '.join(result)}**

Parabéns! Você ganhou `${int(self.valor * 0.6)}!`
''',)
            embed.set_footer(text=f'+ {random.randint(2, 5)} XP')

# * SEM COMBINAÇÕES
        else:
            saldos[self.user_id][0] -= self.valor
            save_saldos(saldos)

            embed = discord.Embed(color=discord.Color.red(), title='🎰 Caça-níquel', description=
f'''
{sc.user.display_name} Puxou a alavanca

**Você conseguiu:**
**{' • '.join(result)}**

Mais sorte na próxima! Você perdeu `${self.valor}!`
''',)
        
        await sc.response.send_message(embed=embed)


class cacaniquel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='caça-níquel', description='🎰 Apostas | Aposte no caça-níquel')
    @app_commands.describe(valor='Valor da aposta')
    async def cacaniquel(self, sc: discord.Interaction, valor: int):
        if valor > 15000:
            await sc.response.send_message('❗ | Calma aí parça, isso tudo? Aposta um pouco menos', ephemeral=True)
            return
        if valor <= 3:
            await sc.response.send_message(f'❗ | O valor precisa ser maior que três', ephemeral=True)
            return
        user_id = str(sc.user.id)

        view = apostar(valor=valor, user_id=user_id)
        await sc.response.send_message(f'🎰 | {sc.user.display_name}, você quer mesmo apostar `${valor}` no caça-níquel?', view=view)
    

      
        

    

async def setup(bot):
    await bot.add_cog(cacaniquel(bot))