#basicamente abaixo você já tem tudo que precisa pra enviar a imagem
import discord
from discord.ext import commands
import json
from gerador import gerarImagemMain, gerarImagemAvatar
from time import sleep

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
    await gerarImagemMain()
    sleep(1)
    await ctx.send('IMAGEM GERADA AQUI')
    await ctx.send(file=discord.File('images\gerada.jpg'))

#aposetando por enquanto essa funcionalidade
@bot.command()
async def avatar(ctx:commands.Context, avatarID):
    from io import BytesIO
    from requests import get

    from PIL import Image
    user = await bot.fetch_user(avatarID)
    if user is None:
        await ctx.send('NÃO FOI POSSIVEL ENCONTRAR O USUARIO')
    else:
        avatarURL = user.avatar
        response = get(avatarURL)
        imagemPillow = Image.open(BytesIO(response.content))
        gerarImagemAvatar(imagemPillow)
        sleep(1)
        await ctx.send('IMAGEM GERADA AQUI')
        await ctx.send(file=discord.File('images\gerada.jpg'))

@bot.event
async def on_ready():
    print("INICIANDO FUNCIONAMENTO")
    print(f'Logado como {bot.user}!')

@bot.event
async def on_member_join(member):
    await member.send('Bem vindo ao servidor teste do Link! {member.mention}')

#* TOKEN DO BOT
bot.run(TOKEN_BOT)