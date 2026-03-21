import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_menu(day_to_search=None):
    url = "https://www.pucsp.br/cardapio-da-semana"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Erro ao acessar o site da PUC-SP: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    
    if not table:
        return "Tabela de cardápio não encontrada no site."

    rows = table.find_all("tr")
    
    # Se não informar o dia, usa o de hoje
    if day_to_search is None:
        day_to_search = datetime.now().strftime("%d")
    
    # Garante que o dia é uma string de 2 dígitos (ex: "05", "23")
    day_to_search = str(day_to_search).zfill(2)
    
    # A estrutura da tabela:
    # Row 0: Header
    # Rows 1, 3, 5...: Datas
    # Rows 2, 4, 6...: Cardápios
    
    found_menu = None
    
    for i in range(1, len(rows), 2):
        date_row = rows[i]
        menu_row = rows[i+1] if i+1 < len(rows) else None
        
        # Procura o dia informado nas células da linha de data
        date_cells = date_row.find_all("td")
        for idx, cell in enumerate(date_cells):
            cell_text = cell.get_text(strip=True)
            if cell_text == day_to_search:
                # Achou o dia! Pega a célula correspondente na linha de baixo
                if menu_row:
                    menu_cells = menu_row.find_all("td")
                    if idx < len(menu_cells):
                        found_menu = menu_cells[idx].get_text(separator="\n", strip=True)
                        break
        if found_menu:
            break
            
    if not found_menu:
        return f"Cardápio não encontrado para o dia {day_to_search} (pode ser final de semana ou feriado)."
    
    return found_menu

if __name__ == "__main__":
    # Teste rápido
    print("Buscando cardápio de hoje...")
    print("-" * 20)
    print(get_menu())
