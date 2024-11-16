#basicamente abaixo já tem tudo que voce precisa pra gerar imagens
from PIL import Image
import json
import random
from os import listdir

# lendo a imagem
class Gerador:
  def __init__(self, template, imagens, jsonFile):
    # abrindo o template
    self.template = Image.open(template) #template base

    # buscando os overlays
    self.listImagens = []
  
    if type(imagens) == list: #aqui considera que tem uma lista de imagens
      for n in imagens:
        #! APARENTEMENTE O PILLOW NÃO ENCONTRA A IMAGEM SEM DIZER QUAL O FORMATO
        imagensTest = Image.open(rf'overlays/{n}.jpeg')
        self.listImagens.append(imagensTest)

    else: #aqui considera que a imagem está em pillow open
      self.listImagens.append(imagens)

    self.listConfigs:list = [] #lista de configurações
    configsTemplate = jsonFile #arquivo já lido com with open


    #*###########################################################################
    #* MUITO IMPORTANTE NOTAR QUE O JSON FILE ESTÁ SENDO JOGADO PARA UM ARRAY   #
    #* PORÉM FICARIA MELHOR PUXAR O VALOR PELA CHAVE DO JSON POIS ASSIM FICARIA #
    #* MAIS FACIL DE ESCALAR DIFERENTES QUANTIDADES DE IMAGENS ...              #
    #*###########################################################################

    # scrapping no dict do json para uma list 'listConfigs'
    for itemValue in configsTemplate:
      self.listConfigs.append(configsTemplate[itemValue])
    
  def imagemPronta(self):
    for n in range(self.listConfigs[0]):
      position = (self.listConfigs[(1 * (n + 1))], self.listConfigs[(2 * (n + 1))])
      medidas = (self.listConfigs[(3 * (n + 1))], self.listConfigs[(4 * (n + 1))])
      overlay = self.listImagens[n].resize((medidas))
      
      self.template.paste(overlay, position)
    self.template.save(rf'temporariaFolder/gerada.jpg')

##############################################################
# a logica abaixo serve apenas para testar o codigo aqui     #
# quando importada essa logica migrara para main.py          #
# assim a função imagemPronta() vai returna alguma coisa     #
# ou então salvar alguma imagem encima de outra para depois  #
# capturar no main.py e enviar no server                     #
##############################################################
# IMPORTANTE IMPLEMENTAR UMA FORMA DE LOG, ONDE FICA SALVA QUAL TEMPLATE CONFIG FOI USADA
# E QUAIS OVERLAYS FOI USADA

#if __name__ == '__main__':
def gerarImagemMain():
  # escolhendo a pasta do template, o max do randint recebe o lenght da pasta templates
  templateRandom:str = (f'template{random.randint(1, len(listdir("templates")))}')

  # tentando puxar o json do template, "if not true" a pasta vai ser salva para analise
  try:
    with open(rf'templates/{templateRandom}/templateConfigs.json',
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
  #! APARENTEMENTE O PILLOW NÃO ENCONTRA A IMAGEM SEM ESPECIFICAR O FORMATO
  instancia = Gerador(rf'templates/{templateRandom}/template.png', listOverlays, dadosJson)
  instancia.imagemPronta()

def gerarImagemAvatar(imagemAvatar):

  # escolhendo a pasta do template, o max do randint recebe o lenght da pasta templates
  templateRandom:str = (f'template{random.randint(1, len(listdir("templates")))}')

  # tentando puxar o json do template, "if not true" a pasta vai ser salva para analise
  try:
    with open(rf'./templates/{templateRandom}/templateConfigs.json',
              'r', encoding='utf-8') as jsonFile:
      dadosJson = json.load(jsonFile)

  except Exception as traceE:
    print(f'NÃO FOI POSSIVEL ENCONTRAR O ARQUIVO ".json" NA PASTA {templateRandom} \n' + f'ou mais precisamente {traceE}')

    #! CONSERTAR ERRO ABAIXO, NÃO ESTÁ SALVANDO O .JSON DE PASTA QUEBRADAS
    #with open('logs.json', 'r') as bFolder:
      #dictBFolder = json.load(bFolder)
      #dictBFolder.append(templateRandom)
      #dictBFolder[templateRandom[1]] = traceE

    #with open('bFolders.json', 'w') as bFolder:
      #json.dump(dictBFolder, bFolder, indent=2)

  # ler o configsTemplate para saber quantas imagens tem que puxar
  # essa lógica abaixo vai ficar desativada por enquanto, pois nenhum template está usando mais
  # do que uma imagem

  #listOverlays:list = []
  #for n in range(int(dadosJson['TOTAL_IMAGENS'])):
    #listOverlays.append(random.randint(1, len(listdir('overlays'))))
    #listOverlays.append('')

  # instancia a classe e gera a imagem
  #! APARENTEMENTE O PILLOW NÃO ENCONTRAR A IMAGEM SEM ESPECIFICAR O FORMATO
  instancia = Gerador(rf'templates/{templateRandom}/template.png', imagemAvatar, dadosJson)
  instancia.imagemPronta()