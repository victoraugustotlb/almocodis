import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, time
import scraper

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Configura as intenções (intents) do bot
intents = discord.Intents.default()
# IMPORTANTE: Você precisa habilitar "Message Content Intent" no Discord Developer Portal (Portal do Desenvolvedor)
# em Bot > Privileged Gateway Intents para que o bot possa ler comandos com prefixo (ex: !almoco).
# Se você quiser usar APENAS comandos de barra (/almoco), pode comentar a linha abaixo.
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    # Inicia a tarefa agendada se ela não estiver rodando
    if not daily_menu_post.is_running():
        daily_menu_post.start()
    
    # Sincroniza comandos de barra (slash commands) se necessário
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos.")
    except Exception as e:
        print(e)

@bot.hybrid_command(name="almoco", description="Mostra o cardápio de hoje")
async def almoco(ctx):
    await ctx.defer()
    menu = scraper.get_menu()
    
    embed = discord.Embed(
        title=f"🍴 Cardápio de Hoje - {datetime.now().strftime('%d/%m/%Y')}",
        description=menu,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Fonte: PUC-SP - Campus Marquês de Paranaguá")
    await ctx.send(embed=embed)

@bot.hybrid_command(name="almoco_dia", description="Procura o cardápio por um dia específico do mês (ex: 25)")
async def almoco_dia(ctx, dia: int):
    await ctx.defer()
    menu = scraper.get_menu(day_to_search=dia)
    
    embed = discord.Embed(
        title=f"🍴 Cardápio do dia {str(dia).zfill(2)}",
        description=menu,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Fonte: PUC-SP - Campus Marquês de Paranaguá")
    await ctx.send(embed=embed)

# Tarefa agendada para as 10:00 AM
# Nota: O tempo é em UTC por padrão no discord.py se não especificado, 
# mas faremos a verificação manual do horário local se necessário.
@tasks.loop(time=time(hour=10, minute=0))
async def daily_menu_post():
    # Verifica se hoje é dia de semana (segunda a sexta = 0 a 4)
    if datetime.now().weekday() > 4:
        return # Não posta nos finais de semana

    if not CHANNEL_ID or CHANNEL_ID == "SEU_ID_DO_CANAL_AQUI":
        print("Aviso: CHANNEL_ID não configurado no .env")
        return

    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel:
            menu = scraper.get_menu()
            embed = discord.Embed(
                title=f"📢 Bom dia! Almoço de hoje: - {datetime.now().strftime('%d/%m/%Y')}",
                description=menu,
                color=discord.Color.green()
            )
            embed.set_footer(text="Fonte: PUC-SP")
            await channel.send(embed=embed)
    except Exception as e:
        print(f"Erro ao postar cardápio automático: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no arquivo .env")
    else:
        bot.run(TOKEN)
