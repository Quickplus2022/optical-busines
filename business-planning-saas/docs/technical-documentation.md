# Documentação Técnica - Sistema SaaS de Planejamento de Negócios

## 📋 Visão Geral

Sistema web completo desenvolvido para auxiliar pequenas e médias empresas no planejamento estratégico e financeiro. Construído com arquitetura moderna, escalável e segura.

## 🏗️ Arquitetura do Sistema

### Stack Tecnológico

#### Backend
- **FastAPI** - Framework web Python moderno e performático
- **PostgreSQL** - Banco de dados relacional robusto
- **SQLAlchemy** - ORM para Python
- **Alembic** - Sistema de migrations
- **Pydantic** - Validação de dados
- **JWT** - Autenticação via tokens
- **ReportLab** - Geração de PDFs

#### Frontend
- **React 18** - Biblioteca para interfaces
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **React Router** - Roteamento SPA
- **React Hook Form** - Gestão de formulários
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos interativos

#### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração local
- **PostgreSQL** - Banco de dados

## 🗂️ Estrutura do Projeto

```
business-planning-saas/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints da API
│   │   │   └── v1/
│   │   │       ├── endpoints/ # Rotas organizadas por módulo
│   │   │       └── api.py     # Router principal
│   │   ├── core/              # Configurações centrais
│   │   │   ├── config.py      # Configurações da aplicação
│   │   │   └── security.py    # Autenticação e segurança
│   │   ├── db/                # Configuração do banco
│   │   │   └── database.py    # Setup SQLAlchemy
│   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── user.py        # Usuários e sessões
│   │   │   ├── business.py    # Negócios
│   │   │   ├── supplier.py    # Fornecedores e produtos
│   │   │   ├── financial.py   # Módulo financeiro
│   │   │   ├── strategic.py   # Módulo estratégico
│   │   │   └── report.py      # Relatórios
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negócio
│   │   └── utils/             # Utilitários
│   ├── requirements.txt       # Dependências Python
│   └── Dockerfile            # Container do backend
├── frontend/                  # Aplicação React
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis
│   │   ├── pages/            # Páginas da aplicação
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # Serviços de API
│   │   └── utils/            # Utilitários
│   ├── package.json          # Dependências Node.js
│   └── Dockerfile           # Container do frontend
├── docs/                     # Documentação
│   ├── database-schema.md    # Esquema do banco
│   ├── process-flow.md       # Fluxos de processo
│   └── technical-documentation.md
└── docker-compose.yml        # Orquestração completa
```

## 🔐 Sistema de Autenticação

### Fluxo de Autenticação
1. **Registro/Login** → Validação de credenciais
2. **Token JWT** → Geração de token de acesso
3. **Middleware** → Validação automática em rotas protegidas
4. **Refresh** → Renovação de tokens

### Segurança Implementada
- Hash de senhas com bcrypt
- Tokens JWT com expiração
- Validação de entrada com Pydantic
- Proteção CORS configurada
- Rate limiting (planejado)

## 💾 Modelo de Dados

### Principais Entidades

#### Users (Usuários)
- Dados pessoais e credenciais
- Relacionamento 1:N com negócios
- Controle de ativação/verificação

#### Businesses (Negócios)
- Entidade central do sistema
- Dados completos da empresa
- Relacionamentos com todos os módulos

#### Suppliers (Fornecedores)
- Cadastro completo de fornecedores
- Histórico de preços
- Avaliações e notas

#### Products/Services (Produtos/Serviços)
- Catálogo de produtos/serviços
- Cálculo automático de preços
- Gestão de margens e impostos

#### Financial (Módulo Financeiro)
- Custos fixos e variáveis
- Projeções financeiras
- DRE automático
- Análises de viabilidade

#### Strategic (Módulo Estratégico)
- Análise SWOT estruturada
- Business Model Canvas
- Metas e KPIs
- Acompanhamento de objetivos

## 🔄 Fluxos de Negócio

### 1. Onboarding de Usuário
```
Registro → Verificação → Primeiro Negócio → Tutorial
```

### 2. Criação de Plano de Negócio
```
Dados Básicos → Fornecedores → Produtos → Custos → Projeções → Relatório
```

### 3. Análise Financeira
```
Dados de Entrada → Cálculos → Validação → Visualização → Relatório
```

### 4. Geração de Relatórios
```
Seleção de Dados → Configuração → Processamento → Geração → Download
```

## 📊 Funcionalidades Principais

### ✅ Implementado (MVP)
- [x] Sistema de autenticação completo
- [x] Cadastro e gestão de negócios
- [x] Interface responsiva com Tailwind
- [x] API REST completa
- [x] Estrutura de banco robusta
- [x] Containerização com Docker

### 🚧 Em Desenvolvimento
- [ ] Módulo de fornecedores completo
- [ ] Cálculos financeiros avançados
- [ ] Análise SWOT interativa
- [ ] Business Canvas visual
- [ ] Geração de relatórios PDF
- [ ] Dashboards com gráficos

### 🔮 Roadmap Futuro
- [ ] Integração com APIs bancárias
- [ ] Análises preditivas com IA
- [ ] App mobile
- [ ] Marketplace de consultores
- [ ] Integração com ERPs

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Git

### Execução Rápida
```bash
# Clonar repositório
git clone <repository-url>
cd business-planning-saas

# Executar com Docker Compose
docker-compose up -d

# Aguardar inicialização e acessar:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Documentação API: http://localhost:8000/docs
```

### Execução Manual

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Banco de Dados
```bash
# PostgreSQL local na porta 5432
createdb business_planning_db
```

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/business_planning_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 📈 Performance e Escalabilidade

### Otimizações Implementadas
- Conexão de banco com pool
- Índices otimizados
- Lazy loading de relacionamentos
- Paginação em listagens
- Compressão de assets

### Monitoramento
- Logs estruturados
- Métricas de performance
- Health checks
- Error tracking

## 🧪 Testes

### Estratégia de Testes
- Testes unitários (pytest)
- Testes de integração (FastAPI TestClient)
- Testes de API (Postman/Newman)
- Testes E2E (Playwright - planejado)

### Cobertura de Testes
- Modelos de dados
- Endpoints de API
- Lógica de negócio
- Autenticação

## 🔒 Segurança

### Medidas de Segurança
- Autenticação JWT
- Hash de senhas
- Validação de entrada
- Proteção CORS
- Sanitização de dados
- Rate limiting (planejado)

### Compliance
- LGPD ready
- Auditoria de ações
- Backup de dados
- Criptografia em trânsito

## 📋 API Documentation

### Principais Endpoints

#### Autenticação
- `POST /api/v1/auth/register` - Registro
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Usuário atual
- `POST /api/v1/auth/refresh` - Renovar token

#### Negócios
- `GET /api/v1/businesses` - Listar negócios
- `POST /api/v1/businesses` - Criar negócio
- `GET /api/v1/businesses/{id}` - Obter negócio
- `PUT /api/v1/businesses/{id}` - Atualizar negócio
- `DELETE /api/v1/businesses/{id}` - Excluir negócio

### Códigos de Status
- `200` - Sucesso
- `201` - Criado
- `400` - Erro de validação
- `401` - Não autorizado
- `404` - Não encontrado
- `500` - Erro interno

## 🚨 Troubleshooting

### Problemas Comuns

#### Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Logs do banco
docker-compose logs db
```

#### Erro de CORS
```bash
# Verificar configuração de ALLOWED_ORIGINS
# Reiniciar backend após mudança
```

#### Dependências Node.js
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

## 📞 Suporte e Contribuição

### Para Desenvolvedores
- Seguir padrões de código
- Testes obrigatórios
- Documentação atualizada
- Code review obrigatório

### Estrutura de Commits
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
refactor: refatoração
test: testes
```

## 📈 Métricas e KPIs

### Métricas Técnicas
- Tempo de resposta < 2s
- Disponibilidade > 99.9%
- Cobertura de testes > 80%
- Zero vulnerabilidades críticas

### Métricas de Negócio
- Taxa de conversão
- Tempo de onboarding
- Satisfação do usuário
- Retenção mensal

---

**Desenvolvido para impulsionar o crescimento de pequenas e médias empresas através de planejamento estratégico baseado em dados** 🚀