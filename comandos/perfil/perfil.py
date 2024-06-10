import discord
from discord import app_commands
from discord.ext import commands
import json

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

#* DETALHES
def load_detalhes():
    try:
        with open('./dados/detalhes.json', "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_detalhes(detalhes):
    with open('./dados/detalhes.json', "w") as f:
        json.dump(detalhes, f, indent=4)

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

#* Userbadges
def load_userbadges():
    try:
        with open("./dados/userbadges.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_userbadges(userbadges):
    with open("./dados/fama.json", "w") as f:
        json.dump(userbadges, f, indent=4)

#* Badges
def load_badges():
    try:
        with open("./dados/badges.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

xpemoji = '<a:xp:1246253262533955655>'
famaemoji ='<a:rainbowfire:1246250924486426634>'


class perfil(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='visualizar', description='🛹 Perfil | Veja seu perfil')
    @app_commands.describe(usuario='O usuário')
    async def visualizar(self, sc: discord.Interaction, usuario: discord.User = None):
        if usuario is None:
            usuario = sc.user
        user_id = str(usuario.id)
        xps = load_xps()
        detalhes = load_detalhes()
        famas = load_famas()
        userbadges = load_userbadges()
        badges = load_badges()

        if user_id not in xps:
            xps[user_id] = 0
            save_xps(xps)
        if user_id not in famas:
            famas[user_id] = 0
            save_famas(famas)
        if user_id not in detalhes:
            detalhes[user_id] = ["Perfil", "Sem descrição", "0"]
            save_detalhes(detalhes)
        if detalhes[user_id][2] == "0":
            bdg = ''
        else:
            bdg = f'***{badges[detalhes[user_id][2]]}***'

        rank = sorted(xps.items(), key=lambda item: item[1], reverse=True)

        # Verificar a posição do usuário no ranking
        found = False
        for i, (user, xp_value) in enumerate(rank, start=1):
            if user == user_id:
                lugar_rank = i
                found = True
                break
        if not found:
            return

        embed = discord.Embed(
            title=f'{detalhes[user_id][0]}',
            description=f'''
>>> **{usuario.display_name}** *(@{usuario.name})*
{bdg}
{famaemoji} Fama `{famas[user_id]}`

{xpemoji} XP `{xps[user_id]}`
🏅 Rank ` #{lugar_rank}`

📖 Descrição
```
{detalhes[user_id][1]}
```
''',
            color=discord.Color.dark_embed())
        embed.set_thumbnail(url=usuario.display_avatar)
        
        await sc.response.send_message(embed=embed)
	

    @app_commands.command(name='editar', description='🛹 Perfil | Customize seu perfil')
    async def editar(self, sc: discord.Interaction):
        await sc.response.send_modal(DetalhesModal())



class DetalhesModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Seu Perfil')

    titulo = discord.ui.TextInput(label='Título', max_length=30)
    insignia = discord.ui.TextInput(label='Badge (Código)', placeholder='Exemplo: 12 (Pride)', max_length=2)
    descricao = discord.ui.TextInput(label='Descrição', max_length=200, style=discord.TextStyle.long)
    async def on_submit(self, sc:discord.Interaction):
        detalhes = load_detalhes()
        userbadges = load_userbadges()
        badges = load_badges()
        user_id = str(sc.user.id)

        titulo = str(self.titulo)
        descricao = str(self.descricao)
        insignia = str(self.insignia)



        embed = discord.Embed(title='📝 Perfil editado',
                              description=f'Seu perfil foi editado',
                              color=discord.Color.dark_embed())


        if insignia in userbadges[user_id]:
            detalhes[user_id][2] = insignia
            embed.add_field(name='Badge', value=badges[detalhes[user_id][2]])
        else:
                detalhes[user_id][2] = "0"
                embed.add_field(name='Badge equipada', value='Não foi possível adicionar a badge')
        detalhes[user_id][0] = titulo
        detalhes[user_id][1] = descricao
        embed.add_field(name='Título', value=titulo)
        embed.add_field(name='Descrição', value=f'```\n{descricao}\n```')
        save_detalhes(detalhes)
        await sc.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(perfil(bot))