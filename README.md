# Dashboard de Prospecção Comercial

Sistema de visualização e análise de dados de prospecção comercial com suporte a múltiplos segmentos.

## 📊 Características

- **Dashboard Dinâmico**: Sistema automaticamente detecta e cria abas para novos segmentos
- **Multi-Estados**: Visualização de hospitais por estado (SP, RS, SC, PR)
- **Segmentos Personalizados**: Suporte automático para novos segmentos (Parques, etc.)
- **Oportunidades**: Seção especial para negócios prioritários que precisam acompanhamento
- **Análise Visual**: Gráficos interativos com Chart.js
- **Busca Avançada**: Filtros e busca em tempo real
- **Design Moderno**: Interface responsiva e profissional

## 📁 Estrutura do Projeto

```
Dashboard Comercial/
├── Lista Prospecçao.xlsx      # Arquivo Excel com dados (múltiplas abas)
├── app.py                      # Servidor Flask com upload ⭐ NOVO
├── process_data.py             # Script para processar dados do Excel
├── dashboard_data.json         # Dados processados (gerado automaticamente)
├── index.html                  # Dashboard principal com upload ⭐ ATUALIZADO
├── requirements.txt            # Dependências Python ⭐ NOVO
├── README.md                   # Esta documentação
├── analyze_excel.py            # Script de análise (legado)
├── dashboard.html              # Dashboard antigo (legado)
└── data.json                   # Dados antigos (legado)
```

## 🚀 Como Usar

### Método 1: Com Servidor Flask (Recomendado - Suporta Upload)

```bash
python app.py
```

**Acesse:** http://localhost:5000

**Funcionalidades:**
- ✅ Dashboard interativo completo
- ✅ Upload de arquivo Excel via interface
- ✅ Processamento automático
- ✅ Atualização em tempo real

### Método 2: Processamento Manual (Opcional)

Se preferir processar o Excel manualmente antes de visualizar:

```bash
python process_data.py
```

Este script irá:
- Ler todas as abas do arquivo Excel
- Processar estados (Hospitais SP, RS, SC, PR)
- Processar segmentos automaticamente (Parques, etc.)
- Processar oportunidades prioritárias
- Gerar o arquivo `dashboard_data.json`

## 📋 Estrutura do Excel

O sistema processa automaticamente as seguintes abas:

### Abas de Estados (Hospitais)
- `Hospitais SP`
- `Hospitais RS`
- `Hospitais SC`
- `Hospitais PR`

### Aba de Oportunidades
- `Oportunidades` - Negócios prioritários que precisam acompanhamento especial

### Abas de Segmentos (Dinâmicas)
- `Parques` - ou qualquer outra aba adicional
- O sistema cria automaticamente abas no dashboard para qualquer nova aba no Excel
- **Novas abas são detectadas automaticamente!**

## ➕ Adicionando Novos Segmentos

### Método 1: Via Upload (Interface)

1. **Clique no botão "Novo Upload"** no canto superior direito do dashboard
2. **Selecione ou arraste** seu arquivo Excel atualizado
3. **Clique em "Enviar Arquivo"**
4. **Aguarde o processamento** (automático)
5. **Dashboard será atualizado automaticamente!**

### Método 2: Manual

Para adicionar um novo segmento ao dashboard:

1. **Adicione uma nova aba no Excel** com o nome do segmento (ex: "Shoppings", "Aeroportos", etc.)
2. **Execute o script de processamento**:
   ```bash
   python process_data.py
   ```
3. **Recarregue o dashboard** no navegador (F5)

**É só isso!** O sistema irá:
- Detectar automaticamente a nova aba
- Processar os dados
- Criar uma nova aba no dashboard
- Renderizar tabela com busca integrada

## 📤 Funcionalidade de Upload

O botão **"Novo Upload"** permite atualizar o dashboard sem precisar de linha de comando:

### Características:
- ✅ **Interface visual** - Arraste e solte ou clique para selecionar
- ✅ **Validação automática** - Verifica tipo e tamanho do arquivo
- ✅ **Progresso visual** - Barra de progresso animada
- ✅ **Processamento automático** - Gera dashboard_data.json automaticamente
- ✅ **Atualização em tempo real** - Dashboard recarrega com novos dados
- ✅ **Feedback imediato** - Mostra estatísticas após processamento

### Limites:
- **Tipos aceitos:** .xlsx, .xls
- **Tamanho máximo:** 50MB
- **Processamento:** Automático e seguro

## 📊 Funcionalidades do Dashboard

### 1. Visão Geral
- Métricas principais (Total de Contatos, Ativos, Taxa de Resposta)
- Gráfico de distribuição por UF
- Gráfico de distribuição Público x Privado
- Evolução temporal de contatos
- Status de contratos

### 2. Por Estados
- Filtro por estado (SP, RS, SC, PR)
- Métricas específicas por estado
- Tabela completa com busca
- Indicadores de contratos

### 3. Oportunidades
- Cards especiais para oportunidades prioritárias
- Informações de contato destacadas
- Observações e notas de acompanhamento
- Visual diferenciado para fácil identificação

### 4. Segmentos (Parques, etc.)
- Tabela completa de cada segmento
- Busca em tempo real
- Visualização de até 8 colunas principais
- Total de registros

## 🔄 Atualização de Dados

Sempre que atualizar o arquivo Excel:

1. Execute o processamento:
   ```bash
   python process_data.py
   ```

2. Recarregue o dashboard no navegador (F5)

## 🛠️ Tecnologias

- **Python**: Processamento de dados (Pandas)
- **Flask**: Servidor web para upload e API
- **JavaScript**: Lógica do dashboard
- **Chart.js**: Gráficos interativos
- **HTML/CSS**: Interface do usuário
- **JSON**: Formato de dados intermediário

## 📦 Dependências

### Instalação Rápida

```bash
pip install -r requirements.txt
```

### Ou instalar manualmente:

```bash
pip install pandas openpyxl flask flask-cors
```

**Bibliotecas necessárias:**
- `pandas` - Processamento de dados Excel
- `openpyxl` - Leitura de arquivos .xlsx
- `flask` - Servidor web
- `flask-cors` - Suporte a CORS para API

## 📝 Colunas Importantes

### Hospitais
- NOME
- PÚBLICO / PRIVADO
- GRUPO
- UF / CIDADE
- RESPONSÁVEL
- TELEFONE / E-MAIL
- DATA DO ÚLTIMO CONTATO
- CONTRATO
- DETALHES DO CONTATO

### Parques
- NOME
- GRUPO
- UF / CIDADE
- RESPONSÁVEL
- TELEFONE
- INAUGURAÇÃO
- DETALHES

## 🎨 Personalização

O sistema foi projetado para ser extensível. Para adicionar novas funcionalidades:

1. **Novos Gráficos**: Adicione funções no JavaScript (index.html)
2. **Novos Filtros**: Adicione lógica de filtro nas funções de renderização
3. **Novas Métricas**: Calcule no process_data.py e adicione no dashboard

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se o servidor HTTP está rodando
2. Confirme que o arquivo `dashboard_data.json` foi gerado
3. Verifique o console do navegador (F12) para erros JavaScript

## 🔐 Segurança

- O sistema roda localmente (localhost)
- Não envia dados para servidores externos
- Dados ficam armazenados apenas no seu computador
