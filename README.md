# KnightFight Bot - Automated Game Bot 🤖⚔️# KnightFight Bot - Automated Game Bot

python -m bot.main -> Cria bots, marca bot para ser deletado e ataca de hora em hora a conta principal
python -m bot_battlefield.main -> Faz ataque no battlefield aos zumbis
python -m bot_highscore_tracker.main -> Faz o tracking do ranking do jogo para analise de dados
python -m bot.knife -> Deleta as contas dos bots, após 24h as contas estão disponiveis para serem deletadas.

docker:
docker-compose build battlefield-bot
docker-compose up -d battlefield-bot

exemplo para rodar docker isolado:
docker-compose build battlefield-bot
docker-compose up -d battlefield-bot


Bot automatizado para KnightFight que cria contas, jogadores e ataca oponentes continuamente com gerenciamento inteligente de cooldown.## 📋 Descrição



---KnightFight Bot é um bot automatizado que cria contas, jogadores e ataca oponentes no jogo KnightFight de forma contínua e inteligente, respeitando cooldowns e maximizando chances de sucesso.



## 🚀 Quick Start## 🎯 Características



```bash✅ **Modo Contínuo**: Roda indefinidamente criando novas contas  

# Docker (Recomendado)✅ **Gerenciamento de Cooldown**: Espera automaticamente e ataca no momento ideal  

./docker-quick-start.sh✅ **Docker Ready**: Fácil deploy em qualquer lugar  

✅ **Múltiplas Tentativas**: Tenta atacar até 30x com intervalo de 0.5s  

# Python Local✅ **Screenshots**: Captura telas de cada etapa  

pip install -r bot/requirements.txt✅ **Histórico**: Registra todos os ataques em JSON  

playwright install chromium

python -m bot.main## 🚀 Quick Start

```

### Método 1: Docker (Recomendado) 🐳

---

```bash

## 🎯 Características# 1. Build e run automático

./docker-quick-start.sh

✅ **Modo Contínuo** - Roda indefinidamente criando novas contas  

✅ **Cooldown Inteligente** - Espera automaticamente e ataca no momento ideal  # OU manualmente:

✅ **Docker Ready** - Deploy fácil em qualquer lugar  docker-compose up -d

✅ **30 Tentativas** - Intervalo de 0.5s entre ataques  

✅ **Screenshots** - Captura cada etapa  # Ver logs

✅ **Histórico JSON** - Registra todos os ataques  docker-compose logs -f

```

---

### Método 2: Python Local

## 📖 Documentação

```bash

- **[🐳 Docker Guide](DOCKER_GUIDE.md)** - Deploy completo# 1. Instalar dependências

- **[🔄 Continuous Mode](CONTINUOUS_MODE.md)** - Modo contínuocd bot

- **[📝 Refactoring](REFACTORING_SUMMARY.md)** - Mudançaspip install -r requirements.txt

- **[🧪 Testing](TESTING_GUIDE.md)** - Testes

- **[⚔️ Attack Flow](bot/ATTACK_FLOW.md)** - Fluxo de ataque# 2. Instalar Playwright

playwright install chromium

---

# 3. Executar

## 🎮 Como Funcionacd ..

python -m bot.main

Cada ciclo (loop infinito):```



1. 🆕 Nova conta → 2. 👤 Novo jogador → 3. ⏰ Verifica cooldown  ## 📖 Documentação Completa

4. ⏳ Espera → 5. ⚔️ Ataca (30x) → 6. 💾 Registra → 7. 🔄 Repete

- **[🐳 Docker Guide](DOCKER_GUIDE.md)** - Deploy com Docker (produção)

```- **[🔄 Continuous Mode](CONTINUOUS_MODE.md)** - Como funciona o modo contínuo

CICLO #1: user_xxx@example.com → HenryStormborn9256 → ✅ SUCESSO- **[📝 Refactoring Summary](REFACTORING_SUMMARY.md)** - Mudanças recentes

CICLO #2: user_yyy@example.com → ArthurIronborn4821 → ✅ SUCESSO- **[🧪 Testing Guide](TESTING_GUIDE.md)** - Como testar o bot

CICLO #3: ...- **[⚔️ Attack Flow](bot/ATTACK_FLOW.md)** - Fluxo de ataque detalhado

```

## 🏗️ Estrutura do Projeto

---

```

## 🐳 Deploykf/

├── bot/                        # 🤖 Bot Python

```bash│   ├── main.py                 # Entry point (modo contínuo)

# VPS/Cloud│   ├── requirements.txt        # Dependências Python

ssh user@servidor│   ├── config/                 # Configurações

curl -fsSL https://get.docker.com | sh│   ├── models/                 # Modelos de dados

git clone <repo> && cd knightfight-bot│   ├── services/               # Lógica de negócio

./docker-quick-start.sh│   │   ├── account_service.py  # Criação de contas

│   │   ├── player_service.py   # Criação de jogadores

# Monitorar│   │   ├── attack_scheduler.py # Gerenciamento de ataques

docker-compose logs -f│   │   └── attack_service.py   # Execução de ataques

```│   └── utils/                  # Utilitários

├── bot_data/                   # 💾 Dados persistentes

---│   └── attack_history.json     # Histórico de ataques

├── bot_screenshots/            # 📸 Screenshots

## 🛠️ Comandos├── Dockerfile                  # 🐳 Imagem Docker

├── docker-compose.yml          # 🐳 Orquestração

```bash├── docker-quick-start.sh       # 🚀 Script de instalação rápida

# Docker└── README.md                   # 📖 Este arquivo

docker-compose up -d        # Iniciar```

docker-compose logs -f      # Logs

docker-compose down         # Parar## 🎮 Como Funciona



# Python### Ciclo Completo (Loop Infinito)### Biblioteca Compartilhada (KF.Shared)

python -m bot.main          # Executar- **BrowserService**: Gerenciamento de instâncias do Playwright

cat bot_data/attack_history.json  # Ver histórico- **LoginService**: Lógica de autenticação reutilizável

```- **Models**: Configurações e credenciais

- **Interfaces**: Contratos para padronização

---

## 📦 Instalação

## ⚙️ Configuração

### Pré-requisitos

`bot/config/settings.py`:- .NET 8 SDK

- `COOLDOWN_HOURS = 1` - Tempo entre ataques- Git

- `MAX_AGGRESSIVE_ATTEMPTS = 30` - Tentativas

- `AGGRESSIVE_RETRY_INTERVAL = 0.5` - Intervalo (segundos)### Passos



---1. Clone o repositório:

```bash

## 📊 Monitoramentogit clone <repository-url>

cd kf

```bash```

# Ataques realizados

cat bot_data/attack_history.json | grep -c "success"2. Restaure as dependências:

```bash

# Estatísticasdotnet restore

docker stats knightfight-bot```

```

3. Instale os navegadores do Playwright:

---```bash

# Será necessário após adicionar o pacote Playwright

## 🏗️ Estruturaplaywright install

```

```

bot/4. Configure as credenciais (User Secrets):

├── main.py              # Entry point```bash

├── services/cd src/KF.Worker1

│   ├── attack_scheduler.pydotnet user-secrets init

│   └── attack_service.pydotnet user-secrets set "AutomationConfig:Username" "seu_usuario"

├── config/settings.pydotnet user-secrets set "AutomationConfig:Password" "sua_senha"

└── requirements.txt

cd ../KF.Worker2

bot_data/attack_history.json  # Históricodotnet user-secrets init

bot_screenshots/              # Imagensdotnet user-secrets set "AutomationConfig:Username" "seu_usuario"

```dotnet user-secrets set "AutomationConfig:Password" "sua_senha"

```

---

## 🔧 Configuração

## 📚 Tech Stack

Edite os arquivos `appsettings.json` em cada worker para configurar:

- Python 3.11+- URLs do site

- Playwright (Chromium)- Seletores CSS dos botões

- Docker- Intervalos de execução

- Timeouts e retry policies

---

Exemplo:

**TL;DR:** `./docker-quick-start.sh` → `docker-compose logs -f` 🚀```json

{
  "AutomationConfig": {
    "BaseUrl": "https://exemplo.com",
    "LoginPage": "/login",
    "TargetPage": "/dashboard",
    "ButtonSelector": "#btnAction",
    "IntervalMinutes": 10,
    "Headless": true
  }
}
```

## 🏃 Execução

### Desenvolvimento

Executar Worker1:
```bash
cd src/KF.Worker1
dotnet run
```

Executar Worker2:
```bash
cd src/KF.Worker2
dotnet run
```

### Build
```bash
dotnet build
```

### Testes
```bash
dotnet test
```

## 📝 Próximos Passos

- [ ] Implementar BrowserService
- [ ] Implementar LoginService
- [ ] Configurar Playwright nos workers
- [ ] Adicionar retry policies com Polly
- [ ] Implementar health checks
- [ ] Adicionar logging estruturado com Serilog
- [ ] Criar testes unitários
- [ ] Documentar deployment

## 🔒 Segurança

- **NUNCA** commite credenciais no código
- Use `dotnet user-secrets` para desenvolvimento
- Use variáveis de ambiente ou Azure Key Vault em produção
- Mantenha o `.gitignore` atualizado

## 📄 Licença

[Definir licença]

## 👥 Contribuindo

[Definir guidelines de contribuição]
