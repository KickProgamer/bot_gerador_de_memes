from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import uuid


app = FastAPI()

# Dicionário para armazenar tokens temporários
temp_tokens = {}

#Capturando HTML CONTENT e Enviando para o User
@app.get("/minha-rota/{token}", response_class=HTMLResponse)
async def minha_funcao(token:str):

  # Verifica se o token existe e se não está 
  if token not in temp_tokens or temp_tokens[token] < datetime.now():
    raise HTTPException(status_code=403, detail='Acesso não permitido ou expirado')
  
  # Renderiza o HTML para o usuário configurar algo
  with open("./frontend/index.html", "r", encoding='utf-8') as file:
    html_content = file.read()
  return html_content

# Função de gerar tokens
def gerar_token_temp():
  token = str(uuid.uuid4())
  temp_tokens[token] = datetime.now() + timedelta(minutes=5)
  return token
#Retornando as informações da pagina e tratando-oas
