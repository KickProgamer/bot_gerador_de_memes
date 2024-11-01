#basicamente abaixo você já tem tudo que precisa pra enviar a imagem
import discord
from discord.ext import commands
import json

#* ABRINDO O JSON FILE
with open('configsMain.json', 'r', encoding='utf-8') as jsonFile:
    dadosConfigs = json.load(jsonFile)

#* PERMISSÕES DO DISCORD
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

#* HEADER CONFIGS
bot = commands.Bot(command_prefix=".",
                   intents=permissoes)
    
#* TOKEN
TOKEN_BOT = dadosConfigs['TOKEN']

#* LÓGICA DO CÓDIGO
@bot.command()
async def gerar(ctx:commands.Context):
    await ctx.send('IMAGEM GERADA AQUI')
    await ctx.send(file=discord.File('20-47-30 31-10-2024.jpg'))
    
@bot.event
async def on_ready():
    print("INICIANDO FUNCIONAMENTO")
    print(f'Logado como {bot.user}!')

#* TOKEN DO BOT
bot.run(TOKEN_BOT)