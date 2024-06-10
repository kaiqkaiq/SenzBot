import discord
import random
from discord import app_commands
from discord.ext import commands

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='dado', description='🚬 Outros | Jogue um dado')
    @app_commands.describe(numero='Resultados possíveis')
    async def roll(self, sc: discord.Interaction, numero: int):
        if numero <= 1:
            await sc.response.send_message(f'❗ | O número tem que ser maior que um, como você quer jogar um dado de {numero} lados?', ephemeral=True)
            return
        if numero > 1000:
            await sc.response.send_message(f'❗ | Calma aí amigo, que número alto! Meu limite é mil', ephemeral=True)
            return
        await sc.response.send_message(f'🎲 | {sc.user.display_name} jogou um dado de `{numero}` lados e caiu `{random.randint(1, numero)}`')
    

async def setup(bot):
    await bot.add_cog(Roll(bot))