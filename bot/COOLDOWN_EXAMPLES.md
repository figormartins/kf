# Cooldown Management Examples

## Sistema de Gerenciamento de Cooldown Implementado

O bot agora implementa um sistema inteligente de gerenciamento de cooldown que respeita a regra de **1 hora entre ataques ao Martyn (ID: 522000820)**.

### ✅ Funcionalidades Implementadas

1. **Tracking de Ataques** (`bot/models/attack_tracker.py`)
   - Salva histórico de todos os ataques em `bot_data/attack_history.json`
   - Registra: opponent_id, timestamp, player_name, success

2. **Detecção de Cooldown** 
   - Verifica se passou 1 hora desde o último ataque
   - Calcula tempo restante com precisão
   - Mostra quem foi o último a atacar

3. **Scheduler Inteligente** (`bot/services/attack_scheduler.py`)
   - Aguarda automaticamente até o cooldown terminar
   - Ataca imediatamente quando disponível (corrida contra outros bots)
   - Mostra contagem regressiva a cada minuto

4. **Mensagens Claras**
   - Informa claramente quando cooldown está ativo
   - Mostra próximo horário disponível
   - Explica o motivo de não poder atacar

### 📊 Exemplo de Saída - Com Cooldown

```bash
==================================================
ATTACK PHASE - Checking cooldown...
==================================================

⏰ COOLDOWN ACTIVE
   Cooldown active. Last attack by 'SvenIronside13550' at 2025-10-29 16:02:28. 
   Next available in 48m 49s.
   Next attack available at: 2025-10-29 17:02:28

⏳ WAITING FOR COOLDOWN...
   Current time: 16:13:38
   Attack time:  17:02:28
   Waiting: 48m 49s
   ⏰ Time remaining: 47m 49s
   ⏰ Time remaining: 46m 49s
   ⏰ Time remaining: 45m 49s
   ...
   ⏰ Time remaining: 1m 0s

✅ Cooldown ended - attacking NOW!
Navigating to opponent page (ID: 522000820)...
✅ Attack completed successfully!
✅ Attack recorded at 2025-10-29 17:02:28
```

### 📊 Exemplo de Saída - Sem Esperar Cooldown

```bash
==================================================
ATTACK PHASE - Checking cooldown...
==================================================

⏰ COOLDOWN ACTIVE
   Cooldown active. Last attack by 'SvenIronside13550' at 2025-10-29 16:02:28. 
   Next available in 48m 49s.
   Next attack available at: 2025-10-29 17:02:28

==================================================
PROCESS COMPLETED!
==================================================
Email: user_1761765185@example.com
Username: user_1761765185
Password: KnightFight2025!00R77d2MeXI6uQcp
Player Name: LancelotEarthshaker5209
Name Registered: ✅ Yes
Attack Status: ⏰ Cooldown
Next Available: 2025-10-29 17:02:28
Info: Cooldown active. Last attack by 'SvenIronside13550' at 2025-10-29 16:02:28. 
      Next available in 48m 49s.
Screenshots Saved: 1
==================================================
```

### 📂 Estrutura de Dados - attack_history.json

```json
[
  {
    "opponent_id": "522000820",
    "timestamp": "2025-10-29T16:02:28.429768",
    "player_name": "SvenIronside13550",
    "attack_successful": true
  },
  {
    "opponent_id": "522000820",
    "timestamp": "2025-10-29T17:02:28.123456",
    "player_name": "KayRavenwind57171",
    "attack_successful": true
  }
]
```

### 🚀 Como Usar

#### Opção 1: Aguardar Cooldown (Recomendado)

```bash
# O bot vai esperar até o cooldown terminar e atacar imediatamente
python -m bot.main
```

**Vantagens:**
- Ataca automaticamente quando possível
- Maximiza chances de conseguir o ataque (corrida contra outros bots)
- Não precisa ficar checando manualmente

#### Opção 2: Não Aguardar Cooldown

```python
# Editar bot/main.py:
bot = KnightFightBot(
    headless=BotSettings.HEADLESS,
    wait_for_cooldown=False  # Apenas reporta, não aguarda
)
```

**Ou usar o script de teste:**
```bash
python test_no_wait.py
```

**Vantagens:**
- Apenas cria conta e verifica cooldown
- Não fica travado aguardando
- Útil para testes rápidos

### ⚙️ Configurações

No arquivo `bot/config/settings.py`:

```python
# Attack cooldown settings
ATTACK_COOLDOWN_HOURS = 1  # Martyn pode ser atacado a cada 1 hora
CHECK_INTERVAL_SECONDS = 60  # Verifica a cada 60 segundos se cooldown acabou
```

### 🎯 Estratégia de Race Condition

O bot é otimizado para **atacar o mais rápido possível** quando o cooldown termina:

1. **Aguarda até 5 segundos antes** do cooldown terminar
2. **Entra em modo agressivo** - tentativas a cada 0.5 segundos
3. **Pré-navega** para a página do oponente (economiza tempo)
4. **Tenta atacar repetidamente** até conseguir ou atingir 20 tentativas
5. **Registra o ataque** imediatamente quando consegue

**Configurações do modo agressivo:**
```python
AGGRESSIVE_ATTACK_WINDOW_SECONDS = 5   # Começa 5s antes
AGGRESSIVE_RETRY_INTERVAL = 0.5        # Tenta a cada 0.5s
MAX_AGGRESSIVE_ATTEMPTS = 20           # Até 20 tentativas
```

**Vantagens desta estratégia:**
- ⚡ **Velocidade**: Página já carregada, pronta para atacar
- 🎯 **Precisão**: Múltiplas tentativas garantem captura do momento exato
- 🏆 **Competitividade**: Maior chance de vencer outros bots
- 📊 **Feedback**: Mostra cada tentativa e tempo restante

### Exemplo de Ataque Agressivo

```
⏳ WAITING FOR COOLDOWN...
   Current time: 14:59:50
   Attack time:  15:00:00
   Waiting: 10s
   🎯 Aggressive attack starts 5s before cooldown ends
   
⚡ AGGRESSIVE ATTACK MODE ACTIVATED!
   Trying to attack every 0.5s
   Target time: 15:00:00
   📍 Navigating to opponent page early...
   ✅ Page loaded - ready to attack!
   
   🎯 Attempt 1/20 - Time to target: 4.8s
   🎯 Attempt 2/20 - Time to target: 4.3s
   🎯 Attempt 3/20 - Time to target: 3.8s
   🎯 Attempt 4/20 - Time to target: 3.3s
   🎯 Attempt 5/20 - Time to target: 2.8s
   🎯 Attempt 6/20 - Time to target: 2.3s
   🎯 Attempt 7/20 - Time to target: 1.8s
   🎯 Attempt 8/20 - Time to target: 1.3s
   🎯 Attempt 9/20 - Time to target: 0.8s
   🎯 Attempt 10/20 - Time to target: 0.3s

🎉 ATTACK SUCCESSFUL!
   ✅ Attack recorded at 2025-10-29 14:59:59
   ⚡ Got it 0.2s BEFORE expected cooldown end!
```

Isso maximiza as chances de conseguir o ataque antes de outros bots!

### 📝 Notas Importantes

- ✅ O arquivo `attack_history.json` é portável - pode ser copiado entre máquinas
- ✅ Todos os caminhos são relativos - funciona em qualquer ambiente
- ✅ O cooldown é calculado por opponent_id (pode ter múltiplos alvos)
- ⚠️ Pressione Ctrl+C para interromper a espera do cooldown
