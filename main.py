import threading
from appFastApi import TokenAPI
from bot import runner   # Função que inicia o bot

def iniciarApi():
    app_api = TokenAPI()
    app_api.run(host="0.0.0.0", port=80)

# Função principal que inicia ambos
def main():
    thread_api = threading.Thread(target=iniciarApi)
    thread_bot = threading.Thread(target=runner)

    thread_api.start()
    thread_bot.start()

    # Espera ambos finalizarem
    thread_api.join()
    thread_bot.join()

if __name__ == "__main__":
    main()
