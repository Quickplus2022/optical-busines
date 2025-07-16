# Sistema SaaS de Planejamento de Negócios

Sistema web completo para auxiliar pequenas e médias empresas no planejamento estratégico e financeiro de seus negócios.

## 🚀 Funcionalidades Principais

### 1️⃣ Cadastro de Negócios
- Dados básicos da empresa
- Segmentação de mercado
- Localização e público-alvo
- Suporte a múltiplos negócios por usuário

### 2️⃣ Módulo de Fornecedores e Custos
- Cadastro completo de fornecedores
- Histórico de preços
- Tabela de custos por produto/serviço
- Cálculo automático de margem de lucro
- Gestão de impostos

### 3️⃣ Módulo Financeiro
- Controle de custos fixos e variáveis
- Projeção de faturamento
- Análise de ponto de equilíbrio
- Cálculo de payback, margem e ROI
- Geração automática de DRE

### 4️⃣ Módulo Estratégico
- Análise SWOT interativa
- Modelo Canvas completo
- Gestão de metas e KPIs

### 5️⃣ Relatórios e Dashboards
- Relatórios em PDF e Excel
- Dashboards interativos
- Gráficos de performance

### 6️⃣ Gestão de Usuários
- Autenticação segura
- Controle de permissões
- Histórico de atividades

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web rápido e moderno
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM
- **Alembic** - Migrations
- **JWT** - Autenticação
- **ReportLab** - Geração de PDFs

### Frontend
- **React.js 18** - Interface do usuário
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos interativos
- **React Router** - Navegação
- **Axios** - Cliente HTTP
- **React Hook Form** - Formulários

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **Nginx** - Proxy reverso

## 📁 Estrutura do Projeto

```
business-planning-saas/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints da API
│   │   ├── core/           # Configurações core
│   │   ├── db/             # Configuração do banco
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negócio
│   │   └── utils/          # Utilitários
│   └── tests/              # Testes automatizados
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # Serviços API
│   │   └── utils/          # Utilitários
│   └── public/             # Arquivos estáticos
├── docs/                   # Documentação
└── database/               # Scripts e migrations
```

## 🚀 Como Executar

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd business-planning-saas
```

2. **Backend**
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

3. **Frontend**
```bash
cd frontend
npm install
npm start
```

### Com Docker
```bash
docker-compose up -d
```

## 📊 Fluxo de Dados

1. **Usuário** → Cadastra empresa e configura dados básicos
2. **Fornecedores** → Adiciona fornecedores e produtos/serviços
3. **Custos** → Define custos fixos, variáveis e margens
4. **Projeções** → Cria projeções financeiras e metas
5. **Análises** → Visualiza relatórios e dashboards
6. **Decisões** → Toma decisões baseadas em dados

## 🔒 Segurança

- Autenticação JWT
- Validação de dados com Pydantic
- Proteção CORS configurada
- Sanitização de entradas
- Rate limiting

## 📈 Roadmap

- [ ] Integração com APIs bancárias
- [ ] Análises preditivas com IA
- [ ] App mobile
- [ ] Integração com sistemas contábeis
- [ ] Marketplace de consultores

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, entre em contato através dos canais oficiais.

---

**Desenvolvido para pequenas e médias empresas que buscam crescimento sustentável** 🚀