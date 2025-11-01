# Guia de Configuração do Neon e Deploy no Vercel

## Passo 1: Criar conta no Neon

1. Acesse: https://console.neon.tech/signup
2. Crie uma conta gratuita
3. Crie um novo projeto chamado "dashboard-comercial"

## Passo 2: Obter DATABASE_URL

1. No dashboard do Neon, clique no seu projeto
2. Vá em **Connection Details**
3. Copie a **Connection String** (deve começar com `postgresql://`)
4. A string tem o formato:
   ```
   postgresql://usuario:senha@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```

## Passo 3: Configurar localmente

Execute no terminal:

```bash
# Windows (PowerShell)
copy .env.example .env
notepad .env

# Linux/Mac
cp .env.example .env
nano .env
```

Cole sua DATABASE_URL no arquivo .env e salve.

## Passo 4: Migrar dados locais para o Neon

Execute no terminal:

```bash
python migrate_to_neon.py
```

Este script irá:
- Verificar a conexão com o Neon
- Criar as tabelas necessárias
- Migrar os dados do all_sheets_data.json
- Verificar se tudo foi migrado corretamente

## Passo 5: Configurar DATABASE_URL no Vercel

Execute no terminal:

```bash
vercel env add DATABASE_URL
```

Quando solicitado:
1. Cole a mesma DATABASE_URL que usou no .env
2. Selecione: Production, Preview e Development
3. Confirme

Ou configure pela interface web:
1. Acesse: https://vercel.com/dornelles81s-projects/dashboard-comercial/settings/environment-variables
2. Clique em "Add New"
3. Name: `DATABASE_URL`
4. Value: Cole sua connection string
5. Environment: Selecione todas (Production, Preview, Development)
6. Clique em "Save"

## Passo 6: Fazer novo deploy

Execute no terminal:

```bash
vercel --prod
```

## Passo 7: Testar o dashboard

1. Acesse a URL do deploy (será exibida no terminal)
2. Verifique se os dados estão carregando
3. Teste o upload de uma nova planilha
4. Verifique se a navegação entre abas funciona

## Troubleshooting

### Erro: DATABASE_URL não configurada
```bash
# Verifique se o .env existe
cat .env

# Se não existir, crie a partir do exemplo
cp .env.example .env
```

### Erro de conexão com o Neon
- Verifique se a DATABASE_URL está correta
- Confirme que copiou a string completa (incluindo ?sslmode=require)
- Teste a conexão: `python -c "from database.db import Database; db = Database(); print('OK')"`

### Dados não aparecem no dashboard
- Verifique se a migração foi bem-sucedida: `python migrate_to_neon.py`
- Verifique os logs do Vercel: `vercel logs`
- Teste a API: Acesse https://seu-deploy.vercel.app/api/data

### Upload não funciona
- Verifique se DATABASE_URL está configurada no Vercel
- Verifique os logs: `vercel logs --follow`
- Teste localmente primeiro: `python app_upload.py`
