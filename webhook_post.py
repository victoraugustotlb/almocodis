import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta  # Adicionado timedelta
import scraper

# Carrega as variáveis de ambiente
load_dotenv()
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_webhook_menu():
    if not WEBHOOK_URL or WEBHOOK_URL == "COLOQUE_SUA_WEBHOOK_AQUI":
        print("Erro: DISCORD_WEBHOOK_URL não configurada no .env")
        return

    # --- ALTERAÇÃO 1: Definir a data como AMANHÃ ---
    amanha = datetime.now() + timedelta(days=1)

    # --- ALTERAÇÃO 2: Verificar se AMANHÃ é dia de semana ---
    # Se amanhã for Sábado (5) ou Domingo (6), não envia.
    if amanha.weekday() > 4:
        print(f"Amanhã ({amanha.strftime('%d/%m')}) é final de semana. Pulando...")
        return

    print(f"Buscando cardápio para amanhã ({amanha.strftime('%d/%m/%Y')})...")
    
    # IMPORTANTE: Se o seu 'scraper.get_menu()' aceitar uma data como parâmetro, 
    # você deve passá-la aqui. Ex: menu = scraper.get_menu(amanha)
    menu = scraper.get_menu() 
    
    # Prepara o payload do webhook (Embed)
    data = {
        "embeds": [
            {
                # --- ALTERAÇÃO 3: Título atualizado para "Amanhã" ---
                "title": f"🍴 Cardápio de Amanhã - {amanha.strftime('%d/%m/%Y')}",
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
        print("Cardápio de amanhã enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar webhook: {e}")

if __name__ == "__main__":
    send_webhook_menu()