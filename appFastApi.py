from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime, timedelta
from shutil import copyfileobj
from os.path import join as jn
from os import getcwd as getDir
from os import listdir
from pathlib import Path
from uuid import uuid4
import json
import uvicorn

temp_tokens = {}
UPLOAD_DIR = Path('templates')
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

'''@app.get('/minha-rota/{token}', response_class=HTMLResponse)
async def minha_funcao(token:str):
    # Verifica se o token existe e se não está expirado
  if token not in temp_tokens or temp_tokens[token] < datetime.now():
    raise HTTPException(status_code=403, detail="Acesso não permitido ou expirado")
  else:
    # Renderiza o HTML para o usuário configurar algo
    with open(jn(getDir(), 'pages', 'index.html'), "r", encoding="utf-8") as htmlContent:
      html_content = htmlContent.read()
      return HTMLResponse(content=html_content)
'''

@app.get('/import_template')
async def importTemplate():
  # Renderiza o HTML para o usuário configurar algo
  with open(jn(getDir(), 'pages', 'index.html'), "r", encoding="utf-8") as htmlContent:
    html_content = htmlContent.read()
    return HTMLResponse(content=html_content)

@app.get('/gerar_token')
async def gerar_token():
  token = str(uuid4())
  temp_tokens[token] = datetime.now() + timedelta(minutes=20)
  return {'token': token}

@app.get('/status')
async def status():
  return {'message' : 'A API está funcionando normalmente'}


@app.post('/receber') #resolver erro do UploadFile
async def receber(file: UploadFile = File(...), dados:str = Form(...)):
  how_many_templates = len(listdir(UPLOAD_DIR))
  template_dir = UPLOAD_DIR / f'template{how_many_templates + 1}'
  #if(file):
  template_dir.mkdir(exist_ok=True)
  
  print(template_dir)

  image_template_dir = template_dir / 'template.png'
  json_file_dir = template_dir / 'templateConfigs.json' 

  with image_template_dir.open('wb') as f:
    copyfileobj(file.file, f)
  
  with json_file_dir.open('w') as f:
    json.dump(json.loads(dados), f, ensure_ascii=False)

# Criando a instância e rodando o servidor
if __name__ == "__main__":
  uvicorn.run('appFastApi:app', host='127.0.0.1', port=8000, reload=True)

# ou
def runAPI():#appA = 'appFastApi:app', hostA = '0.0.0.0', portA = 80, reloadA= True):
  uvicorn.run('appFastApi:app', host='0.0.0.0', port=80)