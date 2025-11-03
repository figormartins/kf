# 🔄 Modo Contínuo - Documentação

## 📋 Descrição

O bot agora roda em **modo contínuo permanente**. Cada ciclo completo:

1. 🆕 Cria nova conta
2. 👤 Cria novo jogador
3. ⚔️ Ataca o oponente (espera cooldown se necessário)
4. 🔚 Fecha sessão
5. 🔄 **Recomeça do zero** (volta ao passo 1)

---

## 🚀 Como Usar

### Execução Simples

```bash
cd /home/igor/Documentos/kf
python -m bot.main
```

**Saída esperada:**
```
🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄
BOT STARTED - CONTINUOUS MODE
Creates new accounts and attacks repeatedly
Press Ctrl+C to stop
🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄

============================================================
🔄 CYCLE #1 - 2025-10-30 15:30:00
============================================================

Creating account with the following credentials:
Email: user_1730304600@example.com
Username: user_1730304600
Password: KnightFight2025!xYz...
--------------------------------------------------
...
✅ Cycle #1 completed successfully!

⏳ Waiting 10 seconds before starting cycle #2...

============================================================
🔄 CYCLE #2 - 2025-10-30 16:35:15
============================================================
...
```

### Parar o Bot

Pressione **`Ctrl+C`** no terminal:

```
⚠️  BOT STOPPED BY USER (Ctrl+C)
Total cycles completed: 5
============================================================
```

---

## 🔄 Fluxo de Cada Ciclo

```
CICLO N
├─ 1. NOVA CONTA
│  ├─ Gera credenciais aleatórias
│  ├─ Email: user_TIMESTAMP@example.com
│  ├─ Username: user_TIMESTAMP
│  └─ Password: KnightFight2025!RANDOM
│
├─ 2. NOVO JOGADOR
│  ├─ Gera nome aleatório (ex: "HenryStormborn9256")
│  └─ Registra no jogo
│
├─ 3. ATAQUE
│  ├─ Carrega histórico de attack_history.json
│  ├─ Verifica cooldown contra Martyn (522000820)
│  ├─ SE COOLDOWN ATIVO:
│  │  ├─ Mostra tempo restante
│  │  ├─ Aguarda até 5s antes do fim
│  │  └─ Countdown: 5, 4, 3, 2, 1...
│  ├─ TENTATIVAS CONTÍNUAS:
│  │  ├─ Navega para página do oponente
│  │  ├─ Tenta ataque (máx 30x, intervalo 0.5s)
│  │  └─ Registra sucesso
│  └─ Resultado: ✅ ou ❌
│
├─ 4. FECHAMENTO
│  ├─ Screenshot final
│  ├─ Fecha navegador
│  └─ Limpa sessão
│
└─ 5. PRÓXIMO CICLO
   ├─ Aguarda 10 segundos
   └─ Volta para o passo 1 (NOVA CONTA)
```

---

## ⚙️ Configurações

### Intervalo entre Ciclos

Edite em `bot/main.py`:

```python
# Linha ~180
print(f"\n⏳ Waiting 10 seconds before starting cycle #{cycle + 1}...")
time.sleep(10)  # ← Altere este valor (em segundos)
```

**Opções:**
- `time.sleep(5)` - 5 segundos (mais rápido)
- `time.sleep(30)` - 30 segundos (mais espaçado)
- `time.sleep(60)` - 1 minuto (produção)

### Retry em Caso de Falha

```python
# Linha ~175
if session:
    print(f"\n✅ Cycle #{cycle} completed successfully!")
    bot.print_summary(session)
else:
    print(f"\n⚠️  Cycle #{cycle} failed - retrying in 30s...")
    time.sleep(30)  # ← Tempo de espera antes de retry
    continue
```

---

## 📊 Exemplo de Execução Completa

### Cenário: 3 Ciclos em Sequência

```
🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄
BOT STARTED - CONTINUOUS MODE
Creates new accounts and attacks repeatedly
Press Ctrl+C to stop
🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄

============================================================
🔄 CYCLE #1 - 2025-10-30 15:00:00
============================================================

Creating account: user_1730300400@example.com
✅ Account created
✅ Player created: HenryStormborn9256

🎯 STARTING ATTACK SEQUENCE
✅ NO COOLDOWN - Ready to attack!
🔄 STARTING CONTINUOUS ATTACK ATTEMPTS...
📍 Attempt 1/30
   ✅ Attack sent via Direct Buttons
🎉 ATTACK SUCCESSFUL!

✅ Cycle #1 completed successfully!

==================================================
PROCESS COMPLETED!
==================================================
Email: user_1730300400@example.com
Player Name: HenryStormborn9256
Attack Status: ✅ Success
==================================================

⏳ Waiting 10 seconds before starting cycle #2...

============================================================
🔄 CYCLE #2 - 2025-10-30 16:01:15
============================================================

Creating account: user_1730304075@example.com
✅ Account created
✅ Player created: ArthurIronborn4821

🎯 STARTING ATTACK SEQUENCE
⏰ COOLDOWN ACTIVE
   Next attack available at: 16:00:00
   Waiting for: 58m 45s
   
⏳ Waiting 53m 45s until aggressive window...
⚡ AGGRESSIVE WINDOW - 5s until attack available
   ⏱️  5s...
   ⏱️  4s...
   ⏱️  3s...
   ⏱️  2s...
   ⏱️  1s...

🔄 STARTING CONTINUOUS ATTACK ATTEMPTS...
📍 Attempt 1/30
📍 Attempt 2/30
   ✅ Attack sent via Direct Buttons
🎉 ATTACK SUCCESSFUL!

✅ Cycle #2 completed successfully!

⏳ Waiting 10 seconds before starting cycle #3...

============================================================
🔄 CYCLE #3 - 2025-10-30 17:00:30
============================================================
...
```

---

## 💾 Arquivos Gerados

Cada ciclo gera seus próprios arquivos:

### attack_history.json (Compartilhado)

```json
[
  {
    "opponent_id": "522000820",
    "timestamp": "2025-10-30T15:00:00",
    "player_name": "HenryStormborn9256",
    "success": true
  },
  {
    "opponent_id": "522000820",
    "timestamp": "2025-10-30T16:00:00",
    "player_name": "ArthurIronborn4821",
    "success": true
  },
  {
    "opponent_id": "522000820",
    "timestamp": "2025-10-30T17:00:00",
    "player_name": "WilliamDragonborn7392",
    "success": true
  }
]
```

### Screenshots (Por Ciclo)

```
bot_screenshots/
├── attack_success_150000.png  ← Ciclo 1
├── attack_success_160000.png  ← Ciclo 2
├── attack_success_170000.png  ← Ciclo 3
└── ...
```

---

## 🎯 Vantagens do Modo Contínuo

✅ **Múltiplas Contas**: Cada ciclo cria uma conta nova  
✅ **Maximiza Ataques**: Aproveita cada janela de cooldown  
✅ **Automático**: Não precisa reiniciar manualmente  
✅ **Resiliente**: Retry automático em caso de falha  
✅ **Escalável**: Pode rodar múltiplas instâncias em paralelo  

---

## 🔧 Dicas de Produção

### 1. Executar em Background

```bash
# Com nohup (continua mesmo se fechar terminal)
nohup python -m bot.main > bot.log 2>&1 &

# Ver logs em tempo real
tail -f bot.log

# Parar o bot
pkill -f "python -m bot.main"
```

### 2. Executar com Screen/Tmux

```bash
# Criar sessão screen
screen -S knightfight-bot

# Rodar bot
python -m bot.main

# Detach: Ctrl+A, D

# Reattach
screen -r knightfight-bot
```

### 3. Systemd Service (Linux)

```ini
# /etc/systemd/system/knightfight-bot.service
[Unit]
Description=KnightFight Bot
After=network.target

[Service]
Type=simple
User=igor
WorkingDirectory=/home/igor/Documentos/kf
ExecStart=/usr/bin/python3 -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable knightfight-bot
sudo systemctl start knightfight-bot
sudo systemctl status knightfight-bot
```

---

## 📈 Monitoramento

### Ver Quantos Ataques Foram Feitos

```bash
cat bot_data/attack_history.json | grep -c "success"
```

### Ver Última Execução

```bash
tail -n 50 bot.log
```

### Ver Estatísticas

```python
import json
from datetime import datetime

with open('bot_data/attack_history.json') as f:
    history = json.load(f)

successful = [a for a in history if a.get('success')]
print(f"Total attacks: {len(successful)}")
print(f"Unique players: {len(set(a['player_name'] for a in successful))}")
print(f"First attack: {successful[0]['timestamp']}")
print(f"Last attack: {successful[-1]['timestamp']}")
```

---

## ⚠️ Considerações

1. **Recursos**: Cada ciclo cria um navegador novo. Monitore CPU/RAM
2. **Rate Limiting**: O servidor pode bloquear muitas contas do mesmo IP
3. **Cooldown Compartilhado**: Todos os bots respeitam o mesmo cooldown (1h)
4. **Screenshots**: Podem ocupar muito espaço em disco (limpe periodicamente)

---

## 🎉 Pronto!

Agora o bot roda **continuamente**, criando infinitas contas e atacando automaticamente! 🚀

**Comando:**
```bash
python -m bot.main
```

**Parar:**
```bash
Ctrl+C
```
