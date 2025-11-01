# 🚀 Início Rápido - Deploy do Dashboard

## ⚡ 3 Passos para colocar no ar

### 1️⃣ Configure o banco de dados Neon

Execute este script interativo que vai guiá-lo:

```bash
python configure_database.py
```

O script vai:
- Abrir o console do Neon para você criar uma conta (se ainda não tiver)
- Pedir para você colar a DATABASE_URL
- Testar a conexão
- Criar o arquivo .env
- Migrar seus dados locais

### 2️⃣ Configure no Vercel

Execute um destes comandos:

```bash
# Opção A: Via CLI (mais rápido)
vercel env add DATABASE_URL

# Opção B: Via web interface
# Acesse: https://vercel.com/dashboard
# Vá em: Settings > Environment Variables
# Adicione: DATABASE_URL = <sua-connection-string>
```

### 3️⃣ Faça o deploy

```bash
vercel --prod
```

Pronto! ✅ Seu dashboard estará no ar!

---

## 📋 Checklist completo

- [ ] Criar conta no Neon (https://console.neon.tech/signup)
- [ ] Copiar DATABASE_URL do Neon
- [ ] Executar `python configure_database.py`
- [ ] Confirmar que dados foram migrados
- [ ] Configurar DATABASE_URL no Vercel
- [ ] Executar `vercel --prod`
- [ ] Acessar URL do deploy
- [ ] Testar visualização dos dados
- [ ] Testar upload de nova planilha

---

## 🆘 Problemas?

### Erro: "DATABASE_URL não configurada"
```bash
python configure_database.py
```

### Erro: "Falha ao conectar ao banco"
- Verifique se copiou a DATABASE_URL completa
- Confirme que incluiu `?sslmode=require` no final

### Dados não aparecem no dashboard
```bash
python migrate_to_neon.py
```

### Ver logs de erro do Vercel
```bash
vercel logs --follow
```

---

## 📚 Documentação completa

- `SETUP_NEON.md` - Guia detalhado
- `README.md` - Documentação técnica
- `database/schema.sql` - Estrutura do banco
