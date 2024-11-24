#basicamente abaixo você já tem tudo que precisa pra enviar a imagem
import discord
from discord.ext import commands
import json
from gerador import gerarImagemMain, gerarImagemAvatar
from time import sleep
from asyncio import sleep as sl
from uuid import uuid4
import requests

#* PERMISSÕES DO DISCORD
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

#* HEADER CONFIGS
bot = commands.Bot(command_prefix=".",
                   intents=permissoes)

#* TOKEN
SUB_DOMAIN = 'shitbot.squareweb.app/'
SUB_DOMAIN_LOCAL = 'http://127.0.0.1:8000'

#* LÓGICA DO CÓDIGO
@bot.command()
async def gerar(ctx:commands.Context):
    gerarImagemMain()
    sleep(1)
    await ctx.send('IMAGEM GERADA AQUI')
    await ctx.send(file=discord.File('temporariaFolder/gerada.jpg'), )

#aposetando por enquanto essa funcionalidade
@bot.command()
async def avatar(ctx:commands.Context, avatarID):
    from io import BytesIO
    from PIL import Image
    user = await bot.fetch_user(avatarID)
    if user is None:
        await ctx.send('NÃO FOI POSSIVEL ENCONTRAR O USUARIO')
    else:
        avatarURL = user.avatar
        response = requests.get(avatarURL)
        imagemPillow = Image.open(BytesIO(response.content))
        gerarImagemAvatar(imagemPillow)
        sleep(1)
        await ctx.send('IMAGEM GERADA AQUI')
        await ctx.send(file=discord.File('temporariaFolder/gerada.jpg'))

@bot.command()
async def importar(ctx:commands.Context, t):
    """
    # URL da API na Square Cloud
    API_URL = 'http://shitbot.squareweb.app/'
    API_URL_LOCAL = 'http://127.0.0.1/'

    # Obter token temporário da API
    response = requests.get(API_URL + 'gerar-token')
    data = response.json()
    token = data['token']
    url_temp = f"{API_URL}minha-rota/{token}"
    print('UMA NOVA REQUISIÇÃO DE API FOI REGISTRADA')
    await ctx.send(f"A URL temporária é: {url_temp}")"""
    await ctx.send(f"Devido ao pobre conhecimento do inconpentente do meu dono a url para enviar template permanecerá estática e qualquer um poderá importar template a qualquer momento, até segunda ordem, obrigado \n segue: {SUB_DOMAIN}import_template")


# função para rodar em loop task abaixo
async def enviar_memes_automatico():
    await bot.wait_until_ready()

    #lista de canal futuramente deverá ser personalizada
    target_channel = bot.get_channel(1275586691939307532)

    if target_channel is None:
        print(" Canal de destino não encontrado!")
        return
    
    while not bot.is_closed():
        try:
            gerarImagemMain()
            sleep(3)
            await target_channel.send(f"IMAGEM GERADA AQUI id: {str(uuid4())}")
            await target_channel.send(file=discord.File('temporariaFolder/gerada.jpg'))
            await sl(2 * 60 * 60)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            await sl(60) # aguarda um minuto antes for try again


@bot.event
async def on_ready():
    print("INICIANDO FUNCIONAMENTO")
    print(f'Logado como {bot.user}!')

    bot.loop.create_task(enviar_memes_automatico())
    print('Enviando memes automáticos funcionando')

    # teste se o uvicorn está rodando
    try:
        API_URL = 'https://shitbot.squareweb.app/'
        API_URL_LOCAL = 'http://127.0.0.1:8000/'
        # verifcando o status da API
        responseAPI = requests.get(API_URL + "status")
        if responseAPI.status_code == 200:
            data = responseAPI.json()
            if data.get("message") == "API está funcionando corretamente":
                print("A API está funcionando")
            else:
                print(f"A API respondeu porém não como esperado: {data}")
        else:
            print(f"A API respondeu com erro. Código de status: {responseAPI.status_code}")
    except requests.exceptions.RequestException as e:
        print(f" Erro ao conectar à API: {e}")

@bot.event
async def on_member_join(member):
    await member.send('Bem vindo ao servidor teste do Link! {member.mention}')

#* ABRINDO O JSON FILE
with open('configsMain.json', 'r', encoding='utf-8') as jsonFile:
    dadosConfigs = json.load(jsonFile)

#* TOKEN DO BOT
TOKEN_BOT = dadosConfigs['TOKEN']

def runner():
    bot.run(TOKEN_BOT)

if __name__ == '__main__':
    bot.run(TOKEN_BOT)

