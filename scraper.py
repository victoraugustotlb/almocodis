import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_menu(day_to_search=None):
    url = "https://www.pucsp.br/cardapio-da-semana"
    try:
        # Timeout curto para não travar o GitHub Action se o site da PUC cair
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Erro ao acessar o site da PUC-SP: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    
    if not table:
        return "Tabela de cardápio não encontrada no site (verifique se o site mudou o layout)."

    rows = table.find_all("tr")
    
    # Se não informar o dia, usa o de hoje (mas agora o webhook vai passar o dia de amanhã)
    if day_to_search is None:
        day_to_search = datetime.now().strftime("%d")
    
    # Garante que o dia é uma string de 2 dígitos (ex: "05", "23")
    day_to_search = str(day_to_search).zfill(2)
    
    found_menu = None
    
    # A estrutura da tabela da PUC alterna entre linha de DATA e linha de CONTEÚDO
    for i in range(1, len(rows), 2):
        date_row = rows[i]
        menu_row = rows[i+1] if i+1 < len(rows) else None
        
        date_cells = date_row.find_all("td")
        for idx, cell in enumerate(date_cells):
            cell_text = cell.get_text(strip=True)
            
            # Se o texto da célula for exatamente o dia que buscamos (ex: "26")
            if cell_text == day_to_search:
                if menu_row:
                    menu_cells = menu_row.find_all("td")
                    if idx < len(menu_cells):
                        found_menu = menu_cells[idx].get_text(separator="\n", strip=True)
                        break
        if found_menu:
            break
            
    if not found_menu:
        return f"Cardápio não encontrado para o dia {day_to_search}. (Pode ser que a semana ainda não tenha sido atualizada no site)."
    
    return found_menu