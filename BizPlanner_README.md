# BizPlanner SaaS — Sistema Web de Planejamento de Negócios

Este repositório contém a fundação de um sistema Software-as-a-Service (SaaS) para planejamento de negócios destinado a pequenas e médias empresas.
Ele foi gerado automaticamente como ponto de partida e foca na seguinte stack:

* **Front-end**: React + Vite + TypeScript + TailwindCSS  
* **Back-end**: FastAPI (Python 3.11)  
* **Banco de dados**: PostgreSQL  
* **Geração de PDF**: ReportLab  
* **Infra**: Docker Compose

> Atenção: trata-se apenas de uma estrutura inicial. Ajuste nomes de entidades, campos e regras de negócio conforme a necessidade do projeto real.

## Estrutura de Pastas

```
.
├── backend/               # API FastAPI + modelos de dados
│   ├── app/
│   │   ├── api/           # Rotas e controladores
│   │   ├── core/          # Configurações, middlewares, utilitários
│   │   ├── models/        # Modelos SQLModel
│   │   ├── schemas/       # Esquemas Pydantic
│   │   └── services/      # Camada de serviço / repositórios
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/              # SPA React
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                  # Diagramas Mermaid
│   ├── ERD.mmd
│   ├── ProcessFlow.mmd
│   └── Screens.mmd
└── docker-compose.yml     # Orquestração local
```

## Como Executar Localmente (Docker Compose)

```bash
# 1. Copie .env.example para .env e ajuste senhas/segredos
cp .env.example .env

# 2. Construa e suba os containers
docker compose up --build
```

Endpoints principais:

* Back-end — http://localhost:8000 (Swagger disponível em /docs)  
* Front-end — http://localhost:5173

## Próximos Passos

1. Implementar modelos em `backend/app/models` seguindo o diagrama em `docs/ERD.mmd`.
2. Criar rotas REST em `backend/app/api`.
3. Configurar React Router e páginas descritas em `docs/Screens.mmd`.
4. Escrever testes unitários e de integração.
5. Provisionar ambiente de produção (ex.: AWS, Fly.io, Railway).

## Licença

MIT