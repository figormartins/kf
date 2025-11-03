# 🐳 KnightFight Bot - Docker Guide

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação Rápida](#instalação-rápida)
3. [Uso](#uso)
4. [Configuração Avançada](#configuração-avançada)
5. [Deploy em Produção](#deploy-em-produção)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Pré-requisitos

### Instalação do Docker

#### Linux (Ubuntu/Debian)
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker (evita sudo)
sudo usermod -aG docker $USER

# Reiniciar sessão ou executar
newgrp docker

# Verificar instalação
docker --version
docker-compose --version
```

#### macOS
```bash
# Instalar via Homebrew
brew install --cask docker

# Ou baixar Docker Desktop:
# https://www.docker.com/products/docker-desktop
```

#### Windows
```powershell
# Instalar Docker Desktop:
# https://www.docker.com/products/docker-desktop

# Verificar instalação
docker --version
docker-compose --version
```

---

## 🚀 Instalação Rápida

### 1️⃣ Clonar/Baixar o Projeto

```bash
cd /home/igor/Documentos/kf
```

### 2️⃣ Build da Imagem Docker

```bash
# Build simples
docker build -t knightfight-bot .

# Ou usando docker-compose
docker-compose build
```

**Tempo estimado:** 3-5 minutos (primeira vez)

### 3️⃣ Executar o Bot

```bash
# Método 1: Docker Run
docker run -d \
  --name knightfight-bot \
  -v $(pwd)/bot_data:/app/bot_data \
  -v $(pwd)/bot_screenshots:/app/bot_screenshots \
  knightfight-bot

# Método 2: Docker Compose (Recomendado)
docker-compose up -d
```

---

## 📖 Uso

### Comandos Básicos

#### Iniciar o Bot
```bash
docker-compose up -d
```

#### Ver Logs em Tempo Real
```bash
docker-compose logs -f
```

Saída esperada:
```
knightfight-bot | 🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄
knightfight-bot | BOT STARTED - CONTINUOUS MODE
knightfight-bot | Creates new accounts and attacks repeatedly
knightfight-bot | Press Ctrl+C to stop
knightfight-bot | 🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄
knightfight-bot | 
knightfight-bot | ============================================================
knightfight-bot | 🔄 CYCLE #1 - 2025-10-30 15:30:00
knightfight-bot | ============================================================
```

#### Parar o Bot
```bash
docker-compose down
```

#### Reiniciar o Bot
```bash
docker-compose restart
```

#### Ver Status
```bash
docker-compose ps
```

#### Remover Tudo (Limpar)
```bash
docker-compose down -v
docker rmi knightfight-bot
```

---

## ⚙️ Configuração Avançada

### 1️⃣ Ajustar Recursos (CPU/RAM)

Edite `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'      # ← Máximo 4 CPUs
      memory: 4G       # ← Máximo 4GB RAM
    reservations:
      cpus: '1.0'      # ← Mínimo 1 CPU
      memory: 1G       # ← Mínimo 1GB RAM
```

### 2️⃣ Configurar Variáveis de Ambiente

Crie arquivo `.env`:

```bash
# .env
HEADLESS=true
COOLDOWN_HOURS=1
MAX_AGGRESSIVE_ATTEMPTS=30
AGGRESSIVE_RETRY_INTERVAL=0.5
```

Atualize `docker-compose.yml`:

```yaml
services:
  knightfight-bot:
    env_file:
      - .env
```

### 3️⃣ Configurar Logs

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "50m"    # ← Tamanho máximo por arquivo
    max-file: "10"     # ← Número de arquivos
```

### 4️⃣ Executar Múltiplas Instâncias

```bash
# docker-compose.multi.yml
version: '3.8'

services:
  bot-1:
    build: .
    container_name: knightfight-bot-1
    volumes:
      - ./bot_data:/app/bot_data
      - ./bot_screenshots_1:/app/bot_screenshots
    restart: unless-stopped

  bot-2:
    build: .
    container_name: knightfight-bot-2
    volumes:
      - ./bot_data:/app/bot_data
      - ./bot_screenshots_2:/app/bot_screenshots
    restart: unless-stopped

  bot-3:
    build: .
    container_name: knightfight-bot-3
    volumes:
      - ./bot_data:/app/bot_data
      - ./bot_screenshots_3:/app/bot_screenshots
    restart: unless-stopped
```

Executar:
```bash
docker-compose -f docker-compose.multi.yml up -d
```

---

## 🌐 Deploy em Produção

### 1️⃣ VPS/Cloud (AWS, DigitalOcean, Linode, etc.)

#### Passo 1: Conectar ao Servidor

```bash
ssh user@seu-servidor.com
```

#### Passo 2: Instalar Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Passo 3: Enviar Arquivos

**Opção A: Git**
```bash
git clone https://github.com/seu-usuario/knightfight-bot.git
cd knightfight-bot
```

**Opção B: SCP**
```bash
# No seu computador local
scp -r /home/igor/Documentos/kf user@servidor:/home/user/knightfight-bot
```

#### Passo 4: Executar

```bash
cd knightfight-bot
docker-compose up -d
```

#### Passo 5: Monitorar

```bash
# Ver logs
docker-compose logs -f

# Ver status
docker-compose ps

# Parar (se necessário)
docker-compose down
```

---

### 2️⃣ Deploy com Auto-Restart (Systemd)

Criar arquivo `/etc/systemd/system/knightfight-bot.service`:

```ini
[Unit]
Description=KnightFight Bot Docker Container
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/user/knightfight-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl enable knightfight-bot
sudo systemctl start knightfight-bot
sudo systemctl status knightfight-bot
```

---

### 3️⃣ Deploy em Kubernetes (Opcional)

```yaml
# knightfight-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knightfight-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: knightfight-bot
  template:
    metadata:
      labels:
        app: knightfight-bot
    spec:
      containers:
      - name: bot
        image: knightfight-bot:latest
        resources:
          limits:
            memory: "2Gi"
            cpu: "2000m"
          requests:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: bot-data
          mountPath: /app/bot_data
        - name: screenshots
          mountPath: /app/bot_screenshots
      volumes:
      - name: bot-data
        persistentVolumeClaim:
          claimName: bot-data-pvc
      - name: screenshots
        persistentVolumeClaim:
          claimName: screenshots-pvc
```

Deploy:
```bash
kubectl apply -f knightfight-deployment.yaml
```

---

## 🐛 Troubleshooting

### Problema: Container não inicia

**Solução:**
```bash
# Ver logs de erro
docker-compose logs

# Rebuild do zero
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: "Permission denied" nos volumes

**Solução:**
```bash
# Ajustar permissões
sudo chown -R $USER:$USER bot_data bot_screenshots
chmod -R 755 bot_data bot_screenshots
```

### Problema: Playwright não encontra navegador

**Solução:**
```bash
# Rebuild instalando dependências
docker-compose build --no-cache
```

### Problema: Container usa muita RAM

**Solução:**
```yaml
# Ajustar em docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G  # ← Reduzir limite
```

### Problema: Bot não ataca (fica em loop)

**Solução:**
```bash
# Ver logs detalhados
docker-compose logs -f --tail=100

# Entrar no container
docker exec -it knightfight-bot bash

# Verificar arquivos
ls -la bot_data/
cat bot_data/attack_history.json
```

---

## 📊 Monitoramento

### Ver Estatísticas do Container

```bash
# CPU, RAM, Network
docker stats knightfight-bot
```

### Ver Histórico de Ataques

```bash
# Dentro do container
docker exec knightfight-bot cat bot_data/attack_history.json

# No host (se volumes montados)
cat bot_data/attack_history.json | jq
```

### Ver Screenshots

```bash
# Listar screenshots
ls -lh bot_screenshots/

# Ver mais recente
ls -lt bot_screenshots/ | head -5
```

---

## 🎯 Comandos Úteis - Resumo

```bash
# BUILD
docker-compose build                 # Build da imagem
docker-compose build --no-cache      # Build sem cache

# EXECUTAR
docker-compose up -d                 # Iniciar em background
docker-compose up                    # Iniciar (ver logs)

# MONITORAR
docker-compose logs -f               # Ver logs em tempo real
docker-compose ps                    # Ver status
docker stats knightfight-bot         # Ver recursos (CPU/RAM)

# CONTROLE
docker-compose restart               # Reiniciar
docker-compose stop                  # Parar
docker-compose down                  # Parar e remover

# MANUTENÇÃO
docker exec -it knightfight-bot bash # Entrar no container
docker-compose down -v               # Remover tudo + volumes
docker system prune -a               # Limpar tudo (Docker)
```

---

## 📦 Estrutura de Arquivos Docker

```
/home/igor/Documentos/kf/
├── Dockerfile                    # ← Imagem do bot
├── .dockerignore                 # ← Arquivos a ignorar
├── docker-compose.yml            # ← Orquestração
├── bot/                          # ← Código do bot
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   ├── config/
│   ├── models/
│   ├── services/
│   └── utils/
├── bot_data/                     # ← Volume (persistente)
│   └── attack_history.json
└── bot_screenshots/              # ← Volume (persistente)
    └── *.png
```

---

## ✅ Checklist de Deploy

- [ ] Docker instalado (`docker --version`)
- [ ] Docker Compose instalado (`docker-compose --version`)
- [ ] Arquivos copiados para servidor
- [ ] Build executado (`docker-compose build`)
- [ ] Container iniciado (`docker-compose up -d`)
- [ ] Logs verificados (`docker-compose logs -f`)
- [ ] Volumes montados (verificar `bot_data/`)
- [ ] Auto-restart configurado (opcional)
- [ ] Monitoramento configurado (opcional)

---

## 🎉 Conclusão

Agora você pode executar o KnightFight Bot em **qualquer lugar** usando Docker!

**Vantagens:**
✅ Portável (funciona em Linux, macOS, Windows)  
✅ Isolado (não afeta sistema host)  
✅ Escalável (múltiplas instâncias facilmente)  
✅ Fácil deploy (um comando)  
✅ Persistente (dados salvos em volumes)  

**Executar:**
```bash
docker-compose up -d
```

**Parar:**
```bash
docker-compose down
```

**Simples assim!** 🐳
