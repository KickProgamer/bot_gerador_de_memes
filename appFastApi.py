from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from uuid import uuid4

class TokenAPI:
    def __init__(self):
        self.app = FastAPI()
        self.temp_tokens = {}
        
        # Configura as rotas do FastAPI
        self.app.add_api_route("/minha-rota/{token}", self.minha_funcao, methods=["GET"], response_class=HTMLResponse)
        self.app.add_api_route("/gerar-token", self.gerar_token, methods=["GET"])

    async def minha_funcao(self, token: str):
        """Rota que valida o token e renderiza o HTML."""
        # Verifica se o token existe e se não está expirado
        if token not in self.temp_tokens or self.temp_tokens[token] < datetime.now():
            raise HTTPException(status_code=403, detail="Acesso não permitido ou expirado")
        
        # Renderiza o HTML para o usuário configurar algo
        with open("../src/index.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return html_content

    async def gerar_token(self):
        """Gera um token temporário e o armazena com validade de 5 minutos."""
        token = str(uuid4())
        self.temp_tokens[token] = datetime.now() + timedelta(minutes=5)
        return {"token": token}

    def run(self, host="0.0.0.0", port=8000):
        """Roda o servidor Uvicorn com o FastAPI."""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)