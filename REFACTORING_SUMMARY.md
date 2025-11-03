# 🔄 Refatoração do Sistema de Ataque - Resumo

**Data:** 30 de outubro de 2025

## 📋 Objetivo

Simplificar a Fase de Ataque (Fase 4) do bot, tornando-a mais eficiente e com um fluxo linear e claro.

## ✅ Mudanças Implementadas

### 1. **AttackScheduler Simplificado** (`bot/services/attack_scheduler.py`)

#### Antes (Complexo):
- Múltiplos métodos: `try_attack_with_cooldown()`, `_wait_and_attack()`, `_try_attack_repeatedly()`, `_wait_with_updates()`, `_perform_attack()`
- Lógica condicional baseada em `wait_for_cooldown` flag
- Retornava dicionários complexos com múltiplos campos

#### Depois (Simples):
- **Um método principal**: `schedule_attack(player, opponent_id) -> bool`
- **Fluxo linear claro**:
  1. Carrega histórico de ataques (`AttackTracker`)
  2. Verifica cooldown
  3. Espera se necessário (`_wait_with_countdown()`)
  4. Tenta ataque continuamente (`_attempt_attack_continuously()`)
- Retorna **boolean simples**: `True` = sucesso, `False` = falha

### 2. **Main.py Atualizado** (`bot/main.py`)

#### Mudanças:
- ✅ Adicionado `from datetime import datetime`
- ✅ Removido parâmetro `wait_for_cooldown` da classe (sempre espera agora)
- ✅ Chamada simplificada:
  ```python
  attack_success = attack_scheduler.schedule_attack(
      player=player,
      opponent_id=BotSettings.TARGET_OPPONENT_ID
  )
  ```
- ✅ Conversão de `bool` para `dict` compatível com `BotSession`

### 3. **AttackService** (`bot/services/attack_service.py`)
- ✅ Mantido como estava (já otimizado)
- Métodos rápidos: `_try_attack_via_buttons_fast()`, `_try_attack_via_links_fast()`

## 🎯 Novo Fluxo de Execução

```
1. INICIALIZAÇÃO
   └─ Cria diretórios, gera credenciais

2. CRIAÇÃO DE CONTA
   └─ Registra nova conta no jogo

3. CRIAÇÃO DO JOGADOR
   └─ Gera nome aleatório e registra

4. FASE DE ATAQUE ⭐ (SIMPLIFICADA)
   ├─ Carrega histórico (attack_history.json)
   ├─ Verifica cooldown contra oponente
   │
   ├─ SE COOLDOWN ATIVO:
   │  ├─ Calcula tempo de espera
   │  ├─ Aguarda até 5s antes do fim
   │  └─ Mostra countdown
   │
   └─ ATAQUE CONTÍNUO:
      ├─ Navega para página do oponente
      ├─ Tenta ataque (máx 30 tentativas)
      ├─ Intervalo: 0.5s entre tentativas
      ├─ Registra sucesso no histórico
      └─ Retorna True/False

5. FINALIZAÇÃO
   └─ Captura screenshot, imprime resumo
```

## 📊 Benefícios

### ✅ Mais Simples
- Fluxo linear sem condicionais complexas
- Um método principal em vez de 5
- Código mais fácil de ler e manter

### ✅ Mais Eficiente
- Sempre espera cooldown (sem flag confusa)
- Sempre tenta ataque continuamente após cooldown
- Lógica de retry centralizada

### ✅ Mais Claro
- Nomenclatura descritiva
- Logs informativos em cada etapa
- Retorno simples (boolean) em vez de dict complexo

### ✅ Mais Configurável
```python
# Pode customizar facilmente:
attack_success = scheduler.schedule_attack(
    player=player,
    opponent_id=BotSettings.TARGET_OPPONENT_ID,
    max_attempts=50,    # mais tentativas
    interval=0.3        # mais rápido
)
```

## 🔧 Configurações Mantidas

Em `BotSettings` (`bot/config/settings.py`):
- **COOLDOWN**: 1 hora entre ataques
- **AGGRESSIVE_ATTACK_WINDOW_SECONDS**: 5s antes do cooldown
- **MAX_AGGRESSIVE_ATTEMPTS**: 30 tentativas
- **AGGRESSIVE_RETRY_INTERVAL**: 0.5s entre tentativas

## 📝 Logs de Exemplo

```
==================================================
🎯 STARTING ATTACK SEQUENCE
==================================================

⏰ COOLDOWN ACTIVE
   Last attack was at 2025-10-30 16:10:00
   Next attack available at: 17:10:00
   Waiting for: 52m 28s
   Current time: 16:17:32

⏳ Waiting 47m 28s until aggressive window...

⚡ AGGRESSIVE WINDOW - 5s until attack available
   ⏱️  5s...
   ⏱️  4s...
   ⏱️  3s...
   ⏱️  2s...
   ⏱️  1s...

🔄 STARTING CONTINUOUS ATTACK ATTEMPTS...
🎯 Attempting attack every 0.5s (max 30 attempts)
   📍 Navigating to opponent page...
   ✅ Page loaded - ready to attack!

📍 Attempt 1/30
   ⏳ Waiting 0.5s before next attempt...

📍 Attempt 2/30
   ✅ Attack sent via Direct Buttons

🎉 ATTACK SUCCESSFUL!
   ✅ Attack recorded at 2025-10-30 17:10:01
   🎯 Succeeded on attempt 2
```

## 🚀 Como Usar

```bash
cd /home/igor/Documentos/kf
python -m bot.main
```

O bot agora:
1. ✅ Sempre carrega o histórico
2. ✅ Sempre verifica cooldown
3. ✅ Sempre espera se necessário
4. ✅ Sempre tenta ataque continuamente

**Simples. Eficiente. Claro.** 🎯
