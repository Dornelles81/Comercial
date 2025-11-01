# 📊 Dashboard Comercial - Prospecção Multi-Regional

Sistema de dashboard comercial com análise temporal, upload de planilhas Excel e visualizações interativas.

## 🚀 Features

- ✅ Dashboard multi-regional (SP, RS, SC, PR + Parques)
- ✅ Upload e processamento dinâmico de planilhas Excel
- ✅ Gráficos de evolução temporal (últimos 12 meses)
- ✅ Funil de vendas para oportunidades
- ✅ Estatísticas consolidadas e por região
- ✅ Filtros e busca em tempo real
- ✅ Banco de dados PostgreSQL (Neon) para persistência
- ✅ Deploy serverless na Vercel

## 🗄️ Arquitetura

- **Frontend**: HTML/CSS/JavaScript + Chart.js
- **Backend**: Python/Flask (Serverless Functions)
- **Database**: PostgreSQL (Neon)
- **Hosting**: Vercel

## 📦 Deploy na Vercel

### 1️⃣ Criar conta no Neon PostgreSQL

1. Acesse: https://console.neon.tech/signup
2. Crie uma conta (pode usar GitHub)
3. Crie um novo projeto
4. Copie a **Connection String** (começa com `postgresql://...`)

### 2️⃣ Deploy na Vercel

#### Opção A: Via GitHub (Recomendado)

1. Acesse: https://vercel.com/new
2. Importe o repositório GitHub: `Dornelles81/Comercial`
3. Configure as variáveis de ambiente:
   - Clique em "Environment Variables"
   - Adicione: `DATABASE_URL` = `sua_connection_string_do_neon`
4. Clique em "Deploy"

#### Opção B: Via Vercel CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd "D:\Projetos\Dashboard Comercial"
vercel --prod

# Adicionar variável de ambiente
vercel env add DATABASE_URL
# Cole a connection string do Neon quando solicitado
```

### 3️⃣ Inicializar o Banco de Dados

Após o deploy, rode este script para criar as tabelas:

```python
from database.db import Database

db = Database()  # Usa DATABASE_URL automaticamente
db.init_database()
```

Ou via SQL direto no Neon Console:
1. Acesse o Neon Console
2. Vá em "SQL Editor"
3. Cole o conteúdo de `database/schema.sql`
4. Execute

### 4️⃣ Fazer Upload da Primeira Planilha

1. Acesse: `https://seu-projeto.vercel.app`
2. Role até o final da página "Resumo Geral"
3. Faça upload da planilha Excel
4. Aguarde o processamento

## 🛠️ Desenvolvimento Local

### Requisitos

- Python 3.8+
- PostgreSQL (Neon ou local)

### Instalação

```bash
# Clonar repositório
git clone https://github.com/Dornelles81/Comercial.git
cd Comercial

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua DATABASE_URL

# Inicializar banco de dados
python -c "from database.db import Database; Database().init_database()"

# Iniciar servidor Flask (desenvolvimento)
python app_upload.py

# Iniciar servidor HTTP para o frontend
python -m http.server 8000
```

### Acessar

- **Upload**: http://localhost:5000
- **Dashboard**: http://localhost:8000/dashboard_completo.html

## 📊 Estrutura de Dados

### Banco de Dados (PostgreSQL)

- `sheets`: Informações de cada aba da planilha
- `records`: Registros individuais (JSONB)
- `statistics`: Estatísticas agregadas (JSONB)
- `column_mappings`: Mapeamento de colunas detectadas

### Colunas Reconhecidas Automaticamente

- **NOME**: Nome do registro/empresa
- **PÚBLICO / PRIVADO**: Tipo/classificação
- **CIDADE**: Localização
- **DATA DO ÚLTIMO CONTATO**: Data do contato
- **CONTRATO**: Status do contrato
- **GRUPO**: Grupo ou categoria
- **OPER. ESTACIONAMENTO**: Operação de estacionamento

## 🔒 Segurança

- ✅ Planilhas Excel não são commitadas no Git
- ✅ Dados sensíveis armazenados no banco de dados
- ✅ Variáveis de ambiente para credenciais
- ✅ CORS configurado

## 📝 Documentação Adicional

- [GUIA_DE_USO.md](GUIA_DE_USO.md) - Guia completo de uso
- [database/schema.sql](database/schema.sql) - Schema do banco de dados

## 🤖 Tecnologias

- Python 3.8+
- Flask + Flask-CORS
- PostgreSQL (Neon)
- Pandas + OpenPyXL + NumPy
- Chart.js
- Vercel (Serverless)

## 📄 Licença

Projeto privado - Todos os direitos reservados

---

**Desenvolvido com ❤️ para gestão comercial eficiente**

🤖 Generated with [Claude Code](https://claude.com/claude-code)
