# KnightFight Bot - Automated Game Bot

## 📋 Descrição

KnightFight Bot é um bot automatizado que cria contas, jogadores e ataca oponentes no jogo KnightFight de forma contínua e inteligente, respeitando cooldowns e maximizando chances de sucesso.

## 🎯 Características

✅ **Modo Contínuo**: Roda indefinidamente criando novas contas  
✅ **Gerenciamento de Cooldown**: Espera automaticamente e ataca no momento ideal  
✅ **Docker Ready**: Fácil deploy em qualquer lugar  
✅ **Múltiplas Tentativas**: Tenta atacar até 30x com intervalo de 0.5s  
✅ **Screenshots**: Captura telas de cada etapa  
✅ **Histórico**: Registra todos os ataques em JSON  

## 🚀 Quick Start

### Método 1: Docker (Recomendado) 🐳

```bash
# 1. Build e run automático
./docker-quick-start.sh

# OU manualmente:
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Método 2: Python Local

```bash
# 1. Instalar dependências
cd bot
pip install -r requirements.txt

# 2. Instalar Playwright
playwright install chromium

# 3. Executar
cd ..
python -m bot.main
```

## 📖 Documentação Completa

- **[🐳 Docker Guide](DOCKER_GUIDE.md)** - Deploy com Docker (produção)
- **[🔄 Continuous Mode](CONTINUOUS_MODE.md)** - Como funciona o modo contínuo
- **[📝 Refactoring Summary](REFACTORING_SUMMARY.md)** - Mudanças recentes
- **[🧪 Testing Guide](TESTING_GUIDE.md)** - Como testar o bot
- **[⚔️ Attack Flow](bot/ATTACK_FLOW.md)** - Fluxo de ataque detalhado

## 🏗️ Estrutura do Projeto

```
kf/
├── bot/                        # 🤖 Bot Python
│   ├── main.py                 # Entry point (modo contínuo)
│   ├── requirements.txt        # Dependências Python
│   ├── config/                 # Configurações
│   ├── models/                 # Modelos de dados
│   ├── services/               # Lógica de negócio
│   │   ├── account_service.py  # Criação de contas
│   │   ├── player_service.py   # Criação de jogadores
│   │   ├── attack_scheduler.py # Gerenciamento de ataques
│   │   └── attack_service.py   # Execução de ataques
│   └── utils/                  # Utilitários
├── bot_data/                   # 💾 Dados persistentes
│   └── attack_history.json     # Histórico de ataques
├── bot_screenshots/            # 📸 Screenshots
├── Dockerfile                  # 🐳 Imagem Docker
├── docker-compose.yml          # 🐳 Orquestração
├── docker-quick-start.sh       # 🚀 Script de instalação rápida
└── README.md                   # 📖 Este arquivo
```

## 🎮 Como Funciona

### Ciclo Completo (Loop Infinito)### Biblioteca Compartilhada (KF.Shared)
- **BrowserService**: Gerenciamento de instâncias do Playwright
- **LoginService**: Lógica de autenticação reutilizável
- **Models**: Configurações e credenciais
- **Interfaces**: Contratos para padronização

## 📦 Instalação

### Pré-requisitos
- .NET 8 SDK
- Git

### Passos

1. Clone o repositório:
```bash
git clone <repository-url>
cd kf
```

2. Restaure as dependências:
```bash
dotnet restore
```

3. Instale os navegadores do Playwright:
```bash
# Será necessário após adicionar o pacote Playwright
playwright install
```

4. Configure as credenciais (User Secrets):
```bash
cd src/KF.Worker1
dotnet user-secrets init
dotnet user-secrets set "AutomationConfig:Username" "seu_usuario"
dotnet user-secrets set "AutomationConfig:Password" "sua_senha"

cd ../KF.Worker2
dotnet user-secrets init
dotnet user-secrets set "AutomationConfig:Username" "seu_usuario"
dotnet user-secrets set "AutomationConfig:Password" "sua_senha"
```

## 🔧 Configuração

Edite os arquivos `appsettings.json` em cada worker para configurar:
- URLs do site
- Seletores CSS dos botões
- Intervalos de execução
- Timeouts e retry policies

Exemplo:
```json
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
