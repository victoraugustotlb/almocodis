import os
import discord
from dotenv import load_dotenv
from datetime import datetime
import scraper
import asyncio

# Carrega as variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

async def send_menu():
    if not TOKEN or not CHANNEL_ID:
        print("Erro: DISCORD_TOKEN ou CHANNEL_ID não configurados.")
        return

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Bot conectado como {client.user.name} para postagem única.')
        
        # Verifica se hoje é dia de semana (segunda a sexta = 0 a 4)
        # COMENTADO PARA TESTES NO FINAL DE SEMANA
        # if datetime.now().weekday() > 4:
        #     print("Hoje é final de semana. Abortando postagem.")
        #     await client.close()
        #     return

        try:
            channel = client.get_channel(int(CHANNEL_ID))
            if channel:
                menu = scraper.get_menu()
                embed = discord.Embed(
                    title=f"🍴 Cardápio de Hoje - {datetime.now().strftime('%d/%m/%Y')}",
                    description=menu,
                    color=discord.Color.green()
                )
                embed.set_footer(text="Enviado via GitHub Actions")
                await channel.send(embed=embed)
                print("Cardápio enviado com sucesso!")
            else:
                print(f"Erro: Canal com ID {CHANNEL_ID} não encontrado.")
        except Exception as e:
            print(f"Erro ao enviar cardápio: {e}")
        
        await client.close()

    try:
        await client.start(TOKEN)
    except Exception as e:
        print(f"Erro ao iniciar o cliente: {e}")

if __name__ == "__main__":
    asyncio.run(send_menu())
