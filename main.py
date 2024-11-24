import threading
from appFastApi import runAPI
from bot import runner   # Função que inicia o bot

def iniciarApi():
    runAPI() #configs de teste

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
