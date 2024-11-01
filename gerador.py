#basicamente abaixo já tem tudo que voce precisa pra gerar imagens
from PIL import Image
import json
import random
from os import listdir
from datetime import datetime

# lendo a imagem
class Gerador:
  def __init__(self, template, imagens, jsonFile):
    # abrindo o template
    self.template = Image.open(template) #template base

    # buscando os overlays
    self.listImagens = []
    for n in imagens:
      #! APARENTEMENTE O PILLOW NÃO ENCONTRA A IMAGEM SEM DIZER QUAL O FORMATO
      imagensTest = Image.open(rf'overlays\{n}.jpeg')
      self.listImagens.append(imagensTest)

    self.listConfigs:list = [] #lista de configurações
    configsTemplate = jsonFile #arquivo já lido com with open

    # scrapping no dict do json para uma list 'listConfigs'
    for itemValue in configsTemplate:
      self.listConfigs.append(configsTemplate[itemValue])
    
  def imagemPronta(self):
    for n in range(self.listConfigs[0]):
      position = (self.listConfigs[(1 * (n + 1))], self.listConfigs[(2 * (n + 1))])
      self.template.paste(self.listImagens[n], position)
    self.template.save(f"{datetime.now().strftime("%H-%M-%S %d-%m-%Y")}.jpg")

##############################################################
# a logica abaixo serve apenas para testar o codigo aqui     #
# quando importada essa logica migrara para main.py          #
# assim a função imagemPronta() vai returna alguma coisa     #
# ou então salvar alguma imagem encima de outra para depois  #
# capturar no main.py e enviar no server                     #
##############################################################
# IMPORTANTE IMPLEMENTAR UMA FORMA DE LOG, ONDE FICA SALVA QUAL TEMPLATE CONFIG FOI USADA
# E QUAIS OVERLAYS FOI USADA

if __name__ == '__main__':
  # escolhendo a pasta do template, o max do randint recebe o lenght da pasta templates
  templateRandom:str = (f'template{random.randint(1, len(listdir('templates')))}')

  # tentando puxar o json do template, "if not true" a pasta vai ser salva para analise
  try:
    with open(rf'templates\{templateRandom}\templateConfigs.json',
              'r', encoding='utf-8') as jsonFile:
      dadosJson = json.load(jsonFile)

  except Exception as traceE:
    print(f'NÃO FOI POSSIVEL ENCONTRAR O ARQUIVO ".json" NA PASTA {templateRandom}')

    #! CONSERTAR ERRO ABAIXO, NÃO ESTÁ SALVANDO O .JSON DE PASTA QUEBRADAS
    #with open('logs.json', 'r') as bFolder:
      #dictBFolder = json.load(bFolder)
      #dictBFolder.append(templateRandom)
      #dictBFolder[templateRandom[1]] = traceE

    #with open('bFolders.json', 'w') as bFolder:
      #json.dump(dictBFolder, bFolder, indent=2)

  # ler o configsTemplate para saber quantas imagens tem que puxar
  listOverlays:list = []
  for n in range(dadosJson['TOTAL_IMAGENS']):
    listOverlays.append(random.randint(1, len(listdir('overlays'))))
  
  # instancia a classe e gera a imagem
  #! APARENTEMENTE O PILLOW NÃO ENCONTRAR A IMAGEM SEM ESPECIFICAR O FORMATO
  instancia = Gerador(rf'templates\{templateRandom}\template.png', listOverlays, dadosJson)
  instancia.imagemPronta()
