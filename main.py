import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOTTOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='_')

async def carregar_cogs():
    diretorios = {
        'info_outros': './comandos/info_outros',
        'economia': './comandos/economia',
        'apostas': './comandos/apostas',
        'img': './comandos/img',
        'perfil': './comandos/perfil'
    }
    for pasta, caminho in diretorios.items():
        for arquivo in os.listdir(caminho):
            if arquivo.endswith('.py'):
                await bot.load_extension(f'comandos.{pasta}.{arquivo[:-3]}')

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        log_channel_id = 1143270436260565043

        log_channel = bot.get_channel(log_channel_id)
        n = interaction.data['name']
        if log_channel:
            await log_channel.send(f'🗂️ | (`{interaction.user.id}`){interaction.user.name} Usou o comando: {n}')

@bot.event
async def on_ready():
    await carregar_cogs()
    print('📁 Cogs carregados')
    sincs = await bot.tree.sync()
    print(f"📶 | {len(sincs)} SlashCommands sincronizados")
    await bot.change_presence(activity=discord.Game(name=f"/img-aguaviva"))
    print(f'💚 | {bot.user} Ligado e Online')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    
@bot.command()
async def botinfo(ctx:commands.Context):
    if ctx.author.id != 835572752068771860:
        return
        
    ping = bot.latency * 1000

    guilds = []
    servers = bot.guilds

    for guild in servers:
        guilds = guilds + [guild.name]

    embed = discord.Embed(
        title='📄 Informações do Bot',
        description=f'''
**{bot.user}** `{bot.user.id}`

**Ping** {ping:.2f}
**Usuários totais** {sum(guild.member_count for guild in bot.guilds)}
**Servidores** ({len(bot.guilds)})
{guilds}
''',
        color=discord.Color.from_rgb(r=171, g=255, b=0))
    await ctx.reply(embed=embed)

bot.run(token)
