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
SUB_DOMAIN = 'shitbot.squareweb.app/'

#* LÓGICA DO CÓDIGO
@bot.command()
async def gerar(ctx:commands.Context):
    gerarImagemMain()
    sleep(1)
    await ctx.send('IMAGEM GERADA AQUI')
    await ctx.send(file=discord.File('temporariaFolder/gerada.jpg'))

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
        await ctx.send(file=discord.File('temporariaFolder/gerada.jpg'))

@bot.command()
async def importar(ctx:commands.Context):
    import requests

    # URL da API na Square Cloud
    API_URL = 'http://shitbot.squarecloud.app/'

    # Obter token temporário da API
    response = requests.get(API_URL + 'gerar-token')
    data = response.json()
    token = data['token']
    url_temp = f"{API_URL}minha-rota/{token}"
    print('UMA NOVA REQUISIÇÃO DE API FOI REGISTRADA')
    await ctx.send(f"A URL temporária é: {url_temp}")


@bot.event
async def on_ready():
    print("INICIANDO FUNCIONAMENTO")
    print(f'Logado como {bot.user}!')

@bot.event
async def on_member_join(member):
    await member.send('Bem vindo ao servidor teste do Link! {member.mention}')

#* TOKEN DO BOT
bot.run(TOKEN_BOT)