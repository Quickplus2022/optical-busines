# 🚀 Guia de Deployment - Business Planning SaaS

## ⚡ Quick Start

### Execução Local com Docker

```bash
# 1. Clone o repositório
git clone <repository-url>
cd business-planning-saas

# 2. Execute com Docker Compose
docker-compose up -d

# 3. Aguarde a inicialização (cerca de 2 minutos)

# 4. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Documentação API: http://localhost:8000/docs
```

## 🛠️ Setup Manual (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

```bash
# 1. Navegar para o backend
cd backend

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Configurar banco de dados
# Criar banco PostgreSQL: business_planning_db

# 6. Executar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# 1. Navegar para o frontend
cd frontend

# 2. Instalar dependências
npm install

# 3. Executar aplicação
npm start
```

## 🔧 Configuração de Ambiente

### Variáveis de Ambiente Obrigatórias

#### Backend (.env)
```bash
# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost:5432/business_planning_db

# Segurança
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Ambiente
ENVIRONMENT=development
DEBUG=true
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 📊 Verificação de Funcionamento

### 1. Backend Health Check
```bash
curl http://localhost:8000/health
# Retorno esperado: {"status":"healthy","version":"1.0.0"}
```

### 2. Frontend Acessível
- Abrir http://localhost:3000
- Página de login deve carregar
- Teste criar conta e fazer login

### 3. API Documentation
- Acessar http://localhost:8000/docs
- Swagger UI deve carregar com todas as rotas

## 🗄️ Configuração do Banco de Dados

### PostgreSQL Local
```bash
# 1. Instalar PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# 2. Criar usuário e banco
sudo -u postgres psql
CREATE USER business_user WITH PASSWORD 'business_pass';
CREATE DATABASE business_planning_db OWNER business_user;
GRANT ALL PRIVILEGES ON DATABASE business_planning_db TO business_user;
\q

# 3. Verificar conexão
psql -h localhost -U business_user -d business_planning_db
```

### Com Docker (Recomendado)
```bash
# Banco incluído no docker-compose.yml
docker-compose up -d db
```

## 🔐 Configuração de Segurança

### Gerar SECRET_KEY Segura
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Configurar CORS
```python
# No arquivo backend/app/core/config.py
ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Frontend local
    "https://yourdomain.com",     # Produção
    "https://app.yourdomain.com"  # App de produção
]
```

## 🧪 Testes

### Executar Testes do Backend
```bash
cd backend
pytest
```

### Executar Testes do Frontend
```bash
cd frontend
npm test
```

## 📦 Build para Produção

### Frontend Build
```bash
cd frontend
npm run build
# Arquivos gerados em: frontend/build/
```

### Backend Otimizado
```bash
cd backend
# Instalar dependências de produção apenas
pip install --no-dev -r requirements.txt
```

## 🐳 Deployment com Docker

### Produção com Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: business_planning_db
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    restart: always
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/business_planning_db
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
      DEBUG: "false"
    depends_on:
      - db

  frontend:
    build: ./frontend
    restart: always
    environment:
      REACT_APP_API_URL: ${API_URL}

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
```

## 🌐 Deploy na Nuvem

### AWS (Exemplo)
```bash
# 1. Configurar AWS CLI
aws configure

# 2. Build e push para ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# 3. Deploy com ECS/Fargate ou EKS
```

### Heroku (Exemplo)
```bash
# 1. Instalar Heroku CLI
npm install -g heroku

# 2. Login e criar app
heroku login
heroku create business-planning-app

# 3. Add-ons necessários
heroku addons:create heroku-postgresql:hobby-dev

# 4. Deploy
git push heroku main
```

## 🔍 Monitoramento

### Logs
```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Aplicação local
tail -f backend/logs/app.log
```

### Health Checks
```bash
# Verificar status dos serviços
curl http://localhost:8000/health
curl http://localhost:3000  # deve retornar 200
```

## ⚠️ Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão
psql -h localhost -U business_user -d business_planning_db
```

#### 2. Porta já em uso
```bash
# Encontrar processo usando a porta
lsof -i :8000
lsof -i :3000

# Matar processo
kill -9 <PID>
```

#### 3. Dependências do Node.js
```bash
# Limpar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 4. Permissões Docker
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

## 📋 Checklist de Deploy

### Antes do Deploy
- [ ] Testes passando
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados acessível
- [ ] SECRET_KEY única e segura
- [ ] CORS configurado corretamente
- [ ] SSL/HTTPS configurado (produção)

### Após o Deploy
- [ ] Health checks funcionando
- [ ] Frontend carregando
- [ ] API respondendo
- [ ] Autenticação funcionando
- [ ] Banco de dados conectado
- [ ] Logs sem erros críticos

## 📞 Suporte

### Para Problemas Técnicos
1. Verificar logs dos serviços
2. Confirmar configurações de ambiente
3. Testar conectividade de rede
4. Verificar permissões de arquivo

### Recursos Úteis
- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação React](https://reactjs.org/docs/)
- [Guia PostgreSQL](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Sistema pronto para transformar pequenas e médias empresas! 🚀**