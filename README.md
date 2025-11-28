# Aevo Deep Fetch API Middleware

Este projeto é um serviço intermediário (Middleware) construído em Python com FastAPI. O seu objetivo é abstrair a complexidade de comunicação com a API da Aevo Innovate.

Atua como um facilitador para extração de dados (Data Fetching), resolvendo problemas estruturais da API original, como paginação manual e tipagem estrita, além de permitir a troca rápida entre ambientes (ex: produção, homologação) via configuração simples de variáveis de ambiente.

### 🛠️ Pré-requisitos

- Python 3.9+

- Acesso à internet (para comunicar com a API da Aevo)

- Token de API da Aevo (Obtido no menu Integrações da plataforma)

### 📦 Instalação

Clone o repositório:
```
git clone https://github.com/Wesley-Nascimentoo/aevo-deep-fetch.git
cd aevo-deep-fetch
```

Crie um ambiente virtual:
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Instale as dependências:
```
pip install -r requirements.txt
```

### ⚙️ Configuração (Variáveis de Ambiente)

Crie um ficheiro .env na raiz do projeto. Graças à arquitetura dinâmica, não deve expor a URL completa, apenas o nome do seu ambiente (subdomínio).
```
# 1. Defina o subdomínio do seu ambiente Aevo
# Exemplo: Se a sua URL é [https://wesley.aevoinnovate.net/], use apenas "wesley"
AEVO_ENV=seu_ambiente

# 2. Seu Token de Acesso (Privado)
AEVO_TOKEN_API=seu_token_aqui_sem_aspas
```

### ▶️ Como Rodar

Execute o servidor uvicorn:
```
uvicorn main:app --reload
```

O servidor iniciará em ``http://127.0.0.1:8000``.

📖 Documentação da API (Swagger)

O projeto possui documentação interativa automática gerada via OpenAPI. Com o servidor rodando, acesse:
```
Swagger UI (Interativo): http://127.0.0.1:8000/docs

ReDoc (Estático): http://127.0.0.1:8000/redoc
```
