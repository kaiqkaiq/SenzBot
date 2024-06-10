import discord
import random
from discord import app_commands
from discord.ext import commands

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @app_commands.command(name="ask", description="🚬 Outros | O famoso 8 Ball, pergunte algo para mim")
    @app_commands.describe(pergunta="A sua pergunta, que responderei (Respostas de S/N)")
    async def ask(self, sc: discord.Interaction, pergunta: str):
        possiveisr = ['Sinceramente não',
                    'Claro que não, oxi',
                    'Apenas não.',
                    'Concerteza não',
                    'Você realmente acha que sim?',
                    'Nem sei como te responder',
                    'Desculpa, mas sei lá',
                    'Eu acho que não, mas talvez sim, depende, mas tipo assim, não da pra saber',
                    'Depende, depende...',
                    'Depende muito, mas provavelmente não',
                    'Depende muito, mas provavelmente sim',
                    'Acho que sim',
                    'Acho que não',
                    'Sinceramente sim',
                    'Claro que sim, é obvio',
                    'SIM! SIM!',
                    'Sim, com certeza!',
                    'Sim! você ainda tem dúvida?',
                    'É mais facíl voltar com ex',
                    'Ao envés de me fazer esse tipo de pergunta acho que você devia conhecer a carteira de trabalho',
                    'Se você acha',
                    'Peraí tô ocupado, pergunta depois',
                    'É com essas coisas que eu sorreio',
                    'Dei uma risada sincera',
                    'NãoKKKKKKKKKKKKK',
                    'SimKKKKKKKKKKKKK',
                    'Quando eu me sentir burro vou me lembrar do que você tá perguntando',
                    'Vô saber porraKKKK']
        resposta = random.choice(possiveisr)
        await sc.response.send_message(f">>> *\"{pergunta[:200]}\"*\n\n🎱 | {resposta}")

    

async def setup(bot):
    await bot.add_cog(Ask(bot))