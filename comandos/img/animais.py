import discord
from discord import app_commands
from discord.ext import commands
import random
import os

class animais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="aguaviva", description="📷 Imagens | Imagens de Água Viva")
    async def aguaviva(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/aguasvivas/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado águas vivas no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem águas vivas!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🪼 | {random.choice(['Já viu a água viva diária?', 'Amo águas vivas!', 'Sua água viva está servida'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")
        await sc.response.send_message(file=file, embed=embed)


    @app_commands.command(name="cachorros", description="📷 Imagens | Imagens de Cachorros")
    async def cachorro(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/cachorros/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado cachorros no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem cachorros!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🐶 | {random.choice(['Já viu o dog diário?', 'Amo cães!', 'Seu cachorro está servido'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")
        await sc.response.send_message(file=file, embed=embed)


    @app_commands.command(name="guaxinins", description="📷 Imagens | Imagens de Guaxinins")
    async def guaxinim(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/guaxinins/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado guaxinins no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem cachorros!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🦝 | {random.choice(['Já viu o guaxinim diária?', 'Amo guaxinins!', 'Seu guaxinim está servido'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")
        await sc.response.send_message(file=file, embed=embed)


    @app_commands.command(name="lontras", description="📷 Imagens | Imagens de lontras")
    async def lontra(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/lontras/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado lontras no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem lontras!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🦦 | {random.choice(['Já viu a lontra diária?', 'Amo lontras!', 'Sua lontra está servida', 'Lontrinha??'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")

        await sc.response.send_message(file=file, embed=embed)

    
    @app_commands.command(name="ratos", description="📷 Imagens | Imagens de ratos")
    async def rato(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/ratos/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado ratos no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem ratos!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🐀 | {random.choice(['Já viu o rato diário?', 'Ama ratos?', 'Seu rato está servido', 'Um ratão aí, só pra descontrair'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")

        await sc.response.send_message(file=file, embed=embed)


    @app_commands.command(name="gatos", description="📷 Imagens | Imagens de gatos")
    async def gato(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/gatos/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado gatos no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem gatos!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"😸 | {random.choice(['Já viu o gato diário?', 'Amo gatos!', 'Seu fato está servido', 'Esses bixanos viu'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")

        await sc.response.send_message(file=file, embed=embed)


    @app_commands.command(name="corvos", description="📷 Imagens | Imagens de corvos")
    async def corvo(self, sc: discord.Interaction):
        pasta = './comandos/img/Imagens/corvos/'
        image_files = [f for f in os.listdir(pasta) if f.endswith('.jpg')]
        if not image_files:
            await sc.response.send_message('🚫 | Não foi encontrado corvos no sistema, talvez seja um erro, ou realmente não há nenhuma... Ficou sem corvos!')
            return

        imagemaleatoria = random.choice(image_files)
        imagem = os.path.join(pasta, imagemaleatoria)

        embed = discord.Embed(
            title=f"🦦 | {random.choice(['Já viu o corvo?', 'Amo lontras!', 'Seu corvo está servida', 'Sabia que os corvos são super inteligentes?'])}",
            color=discord.Color.from_rgb(165, 76, 254)
        )
        file = discord.File(imagem, filename="image.jpg")
        embed.set_image(url=f"attachment://image.jpg")

        await sc.response.send_message(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(animais(bot))