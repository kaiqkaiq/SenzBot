import discord
from discord import app_commands
from discord.ext import commands

pingruim = '<:idleconnection:1246251058087333908>'
pingbom = '<:goodconnection:1246251176085819512>'

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="ping", description="📶 Info | Veja minha latência")
    async def ping(self, sc: discord.Interaction):
        latency = self.bot.latency * 1000
        if latency < 200:
            pingemoji = pingbom
        else:
            pingemoji = pingruim
        await sc.response.send_message(f' {pingemoji}| Latência: {latency:.2f}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))