# Bot de Almoço PUC-SP (Marquês de Paranaguá)

Este bot do Discord busca automaticamente o cardápio do Restaurante Universitário da PUC-SP (Campus Marquês de Paranaguá) e posta em um canal específico todo dia às 10:00 da manhã.

## Como configurar

1. **Token do Bot**: Você já adicionou o token no arquivo `.env`.
2. **ID do Canal**:
   - Vá no Discord e habilite o "Modo Desenvolvedor" em **Configurações de Usuário > Avançado > Modo Desenvolvedor**.
   - Clique com o botão direito no canal onde o bot deve postar e selecione **Copiar ID do Canal**.
   - Abra o arquivo `.env` e substitua `SEU_ID_DO_CANAL_AQUI` pelo ID copiado.
3. **Habilitar Gateway Intents**: No Discord Developer Portal, em **Bot**, habilite a opção **"Message Content Intent"** (embaixo de Privileged Gateway Intents). Sem isso, o bot não terá permissão para rodar e dará o erro `PrivilegedIntentsRequired`.
4. **Instalar Dependências**: Já instalei para você, mas se precisar reinstalar: `pip install -r requirements.txt`

## Como rodar o bot

Abra um terminal na pasta do projeto e execute:
```bash
python bot.py
```

## Comandos
- `/almoco`: Mostra o cardápio de hoje imediatamente.
- `/almoco_dia [dia]`: Procura o cardápio de um dia específico do mês atual (ex: `/almoco_dia 25`).

## Postagem Automática
O bot está configurado para postar o cardápio automaticamente às **10:00 AM** (horário do sistema onde o bot estiver rodando). Ele pula sábados e domingos.

---
**Desenvolvido com Antigravity.**
