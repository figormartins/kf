# KnightFight Bot

Automated account creation, player naming, and attack bot for KnightFight game with **intelligent cooldown management**.

## Project Structure

```
bot/
├── config/               # Configuration and settings
│   ├── __init__.py
│   └── settings.py      # URLs, timeouts, selectors, cooldown settings
├── models/              # Data models
│   ├── __init__.py
│   ├── entities.py      # AccountCredentials, Player, AttackResult, BotSession
│   └── attack_tracker.py # Attack tracking and cooldown management
├── services/            # Business logic services
│   ├── __init__.py
│   ├── account_service.py   # Account registration
│   ├── player_service.py    # Player creation and naming
│   ├── attack_service.py    # Attack operations
│   └── attack_scheduler.py  # Attack scheduling with cooldown
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── generators.py        # Name and credentials generation
│   └── screenshot_manager.py # Screenshot and HTML capture
├── main.py              # Main entry point
└── requirements.txt     # Python dependencies
```

## Features

- ✅ Automated account creation
- ✅ Random unique player name generation (concatenated format)
- ✅ Player name registration
- ✅ Automated opponent search and attack
- ✅ **Intelligent cooldown management** (1-hour attack limit per opponent)
- ✅ **Attack scheduling** - waits and attacks immediately when cooldown ends
- ✅ **Attack history tracking** - prevents attacking during cooldown
- ✅ **Race condition handling** - attacks as fast as possible after cooldown
- ✅ Screenshot capture at each step
- ✅ HTML page analysis for debugging
- ✅ Well-organized code structure
- ✅ English function and variable names
- ✅ Separated concerns (services, models, utils)
- ✅ **Portable - works on any machine** (relative paths)
- ✅ Type hints and comprehensive documentation

## Installation

```bash
# Clone or navigate to project
cd /path/to/kf

# Install dependencies
pip install -r bot/requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

### Run the bot
```bash
# Bot will automatically handle everything:
# 1. Create account
# 2. Create player
# 3. Wait for cooldown if necessary
# 4. Attack continuously until success
python -m bot.main
```

**Note:** Works from any location - uses relative paths!

## Cooldown Management

O bot implementa gerenciamento inteligente de cooldown para cumprir a **regra de limite de 1 hora entre ataques**:

### Como Funciona (Fluxo Simplificado)

1. **Carrega Histórico**: Lê `bot_data/attack_history.json` automaticamente
2. **Verifica Cooldown**: Checa se já atacou Martyn (ID: 522000820) na última hora
3. **Espera se Necessário**: Aguarda até 5 segundos antes do cooldown expirar
4. **Ataque Contínuo**: Tenta atacar repetidamente a cada 0.5s até conseguir
5. **Registra Sucesso**: Salva timestamp do ataque bem-sucedido

### Vantagens

✅ **Totalmente Automático**: Não precisa configurar nada  
✅ **Sempre Espera**: Garante que respeita o cooldown  
✅ **Sempre Tenta**: Ataque contínuo maximiza chances de sucesso  
✅ **Simples**: Um único comando executa tudo  

### Configurações

Ajuste em `bot/config/settings.py`:

```python
COOLDOWN_HOURS = 1                    # Tempo de cooldown
AGGRESSIVE_ATTACK_WINDOW_SECONDS = 5  # Começa a tentar 5s antes
MAX_AGGRESSIVE_ATTEMPTS = 30          # Máximo de tentativas
AGGRESSIVE_RETRY_INTERVAL = 0.5       # Intervalo entre tentativas
```

### Por Que Cooldown Management?

**Problema identificado:** Martyn só pode receber ataque de 1 em 1 hora. O bot precisa:
- ✅ Salvar o momento que o Martyn foi atacado
- ✅ Aguardar até alguns segundos antes do cooldown expirar
- ✅ Tentar atacar repetidamente (a cada 0.5s) para garantir que consegue o ataque
- ✅ Vencer a corrida contra outros bots que também estão tentando atacar

### Example Output with Cooldown:

```
==================================================
ATTACK PHASE - Checking cooldown...
==================================================
⏰ COOLDOWN ACTIVE
   Cooldown active. Last attack by 'ThorThunderfist687950' at 2025-10-29 14:30:15. 
   Next available in 45m 23s.
   Next attack available at: 2025-10-29 15:30:15

⏳ WAITING FOR COOLDOWN...
   Current time: 14:44:52
   Attack time:  15:30:15
   Waiting: 45m 23s
   🎯 Will start trying to attack 5s before cooldown ends
   ⏰ Time remaining: 44m 23s
   ⏰ Time remaining: 43m 23s
   ...
   ⏰ Time remaining: 1m 0s
   ⏰ Time remaining: 5s

⚡ STARTING ATTACK ATTEMPTS!
   Trying every 0.5s until successful
   Target cooldown end: 15:30:15
   📍 Navigating to opponent page...
   ✅ Page loaded - ready to attack!
   🎯 Attempt 1/20 - Time to cooldown end: 4.8s
   🎯 Attempt 2/20 - Time to cooldown end: 4.3s
   🎯 Attempt 3/20 - Time to cooldown end: 3.8s
   🎯 Attempt 4/20 - Time to cooldown end: 3.3s
   🎯 Attempt 5/20 - Time to cooldown end: 2.8s
   ...
   🎯 Attempt 10/20 - Time to cooldown end: 0.3s

🎉 ATTACK SUCCESSFUL!
   ✅ Attack recorded at 2025-10-29 15:30:14
   ⚡ Got it 0.7s BEFORE expected cooldown end!
```
Navigating to opponent page (ID: 522000820)...
✅ Attack completed successfully!
✅ Attack recorded at 2025-10-29 15:30:15
```

### Attack Button Not Found?

When the bot reports "⚠️ No attack button found", it could be:
- **Cooldown active**: Shows who attacked last and when you can attack again
- **Insufficient resources**: New accounts may lack troops/resources
- **Already under attack**: Button is hidden if someone else is attacking

The bot will automatically handle cooldown by waiting and trying repeatedly when the time comes.

## Configuration

Edit `config/settings.py` to customize:
- Target opponent ID
- URLs and endpoints
- Timeouts
- **Attack cooldown hours** (default: 1 hour)
- **Check interval** (default: 60 seconds)
- **Attack window** (default: 5 seconds - starts trying before cooldown ends)
- **Retry interval** (default: 0.5 seconds - time between attack attempts)
- **Max attempts** (default: 20 attempts)
- Screenshot paths
- Browser settings (headless mode)

## Architecture

Follows similar patterns to the C# KF.Mission project:
- **Config**: Centralized configuration (similar to appsettings.json)
- **Models**: Data entities including attack tracking
- **Services**: Business logic separated by concern
- **Utils**: Reusable utility functions
- **Scheduler**: Time-based attack management

## Example Output

```
Creating account with the following credentials:
Email: user_1761689237@example.com
Username: user_1761689237
Password: KnightFight2025!snQ9jnaTxQ8oGwBk
--------------------------------------------------
Navigating to site...
✅ Account created successfully!
Generated player name: HenryStormborn9256
✅ Name registered!
✅ Attack performed!

==================================================
PROCESS COMPLETED!
==================================================
Email: user_1761689237@example.com
Username: user_1761689237
Password: KnightFight2025!snQ9jnaTxQ8oGwBk
Player Name: HenryStormborn9256
Attack Status: ✅ Success
Screenshots Saved: 4
==================================================
```

## Screenshots

All screenshots and HTML files are saved to:
`bot_screenshots/`

All data files saved to:
`bot_data/`

- `before_name_{timestamp}.png` - Before player name selection
- `opponent_{timestamp}.png` - Opponent page
- `opponent_{timestamp}.html` - Opponent page HTML
- `post_attack_{timestamp}.png` - After attack
- `final_registration_{timestamp}.png` - Final state
- `attack_history.json` - Attack tracking data
