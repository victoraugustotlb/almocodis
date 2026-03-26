import os
import requests
import pytz  # Adicione esta importação
from dotenv import load_dotenv
from datetime import datetime, timedelta
import scraper

# Carrega as variáveis de ambiente
load_dotenv()
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_webhook_menu():
    if not WEBHOOK_URL or "discord.com/api/webhooks" not in WEBHOOK_URL:
        print("Erro: DISCORD_WEBHOOK_URL inválida.")
        return

    # --- CORREÇÃO DE FUSO HORÁRIO ---
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora_br = datetime.now(fuso_br)
    
    # Agora, amanhã será SEMPRE o dia seguinte ao de Brasília
    amanha = agora_br + timedelta(days=1)
    
    # Se amanhã for fim de semana, interrompe
    if amanha.weekday() > 4:
        print(f"Amanhã ({amanha.strftime('%d/%m')}) é fim de semana. Pulando...")
        return

    dia_alvo = amanha.strftime("%d")
    data_formatada = amanha.strftime("%d/%m/%Y")

    print(f"Buscando cardápio para o dia {dia_alvo} (Horário de Brasília: {agora_br.strftime('%H:%M')})...")
    
    menu = scraper.get_menu(day_to_search=dia_alvo)
    
    payload = {
        "embeds": [
            {
                "title": f"🍴 Cardápio de Amanhã - {data_formatada}",
                "description": menu,
                "color": 3066993,
                "footer": {
                    "text": "Libriverse Bot • GitHub Actions"
                }
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"Sucesso! Cardápio de {data_formatada} enviado.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    send_webhook_menu()