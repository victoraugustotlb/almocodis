import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import scraper

# Carrega as variáveis de ambiente
load_dotenv()
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_webhook_menu():
    if not WEBHOOK_URL or WEBHOOK_URL == "COLOQUE_SUA_WEBHOOK_AQUI":
        print("Erro: DISCORD_WEBHOOK_URL não configurada no .env")
        return

    # Verifica se hoje é dia de semana (segunda a sexta = 0 a 4)
    # COMENTADO PARA TESTES NO FINAL DE SEMANA
    # if datetime.now().weekday() > 4:
    #     print("Hoje é final de semana. Nenhuma mensagem será enviada.")
    #     return

    print("Buscando cardápio...")
    menu = scraper.get_menu()
    
    # Prepara o payload do webhook (Embed)
    data = {
        "embeds": [
            {
                "title": f"🍴 Cardápio de Hoje - {datetime.now().strftime('%d/%m/%Y')}",
                "description": menu,
                "color": 3066993, # Verde
                "footer": {
                    "text": "Postado automaticamente via GitHub Actions (Webhook)"
                }
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("Cardápio enviado com sucesso via Webhook!")
    except Exception as e:
        print(f"Erro ao enviar webhook: {e}")

if __name__ == "__main__":
    send_webhook_menu()
