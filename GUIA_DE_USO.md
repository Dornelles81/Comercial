# 📊 Dashboard Comercial - Guia de Uso

Sistema de dashboard comercial multi-regional com importador automático de planilhas Excel.

## 🚀 Recursos

- ✅ **Detecção Automática de Abas**: Processa automaticamente todas as abas da planilha Excel
- ✅ **Upload via Web**: Interface web moderna para fazer upload de novas planilhas
- ✅ **Estatísticas Dinâmicas**: Gera estatísticas automaticamente baseadas na estrutura dos dados
- ✅ **Dashboard Interativo**: Visualizações com gráficos e tabelas filtráveis
- ✅ **Funil de Vendas**: Aba especial "Oportunidades" com visualização de funil
- ✅ **Escalável**: Suporta qualquer número de abas e estruturas variadas

---

## 📋 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 🎯 Como Usar

### Método 1: Upload via Interface Web (Recomendado)

#### Passo 1: Iniciar o Servidor de Upload

```bash
python app_upload.py
```

O servidor iniciará em: **http://localhost:5000**

#### Passo 2: Iniciar o Servidor HTTP para o Dashboard

Em outro terminal:

```bash
python -m http.server 8000
```

#### Passo 3: Fazer Upload da Planilha

1. Acesse: **http://localhost:5000**
2. Clique na área de upload ou arraste o arquivo Excel
3. Clique em "Fazer Upload"
4. Aguarde o processamento
5. Acesse o dashboard: **http://localhost:8000/dashboard_completo.html**

---

### Método 2: Processamento Manual via Terminal

```bash
# Processar a planilha padrão
python process_excel_dynamic.py

# Processar uma planilha específica
python process_excel_dynamic.py "caminho/para/sua/planilha.xlsx"
```

---

## 📁 Estrutura de Arquivos

```
Dashboard Comercial/
│
├── app_upload.py                 # Servidor Flask para uploads
├── upload.html                   # Interface de upload
├── process_excel_dynamic.py      # Processador dinâmico de Excel
├── dashboard_completo.html       # Dashboard principal
├── all_sheets_data.json         # Dados processados (gerado automaticamente)
├── requirements.txt             # Dependências Python
├── uploads/                     # Pasta para arquivos enviados
└── GUIA_DE_USO.md              # Este arquivo
```

---

## 🔧 Como Adicionar Novas Abas

O sistema detecta **automaticamente** todas as abas da planilha Excel!

### Basta:
1. Adicionar a nova aba na planilha Excel
2. Fazer upload via interface web OU executar o script de processamento
3. O dashboard será atualizado automaticamente

### O sistema detecta automaticamente:
- ✅ Nome da aba
- ✅ Número de registros
- ✅ Colunas (nome, tipo, cidade, contato, etc.)
- ✅ Estatísticas relevantes
- ✅ Gráficos apropriados

---

## 📊 Estrutura de Dados Recomendada

Para melhor aproveitamento das estatísticas automáticas, use colunas com nomes similares a:

### Colunas Reconhecidas Automaticamente:
- **NOME**: Nome do registro/empresa
- **PÚBLICO / PRIVADO** ou **TIPO**: Classificação do tipo
- **CIDADE**: Localização
- **DATA DO ÚLTIMO CONTATO**: Data do último contato
- **CONTRATO**: Status do contrato
- **GRUPO**: Grupo ou categoria
- **OPER. ESTACIONAMENTO**: Operação de estacionamento
- **COBRA**: Cobrança

> **Nota**: O sistema é flexível e funciona com outras estruturas, mas esses nomes otimizam a geração de estatísticas.

---

## 🎨 Funcionalidades do Dashboard

### 1. Resumo Geral
- Cards com totais consolidados
- Cards de navegação rápida entre abas
- 4 gráficos consolidados:
  - Distribuição por Segmento
  - Status de Contatos Geral
  - Contratos vs Sem Contrato
  - Performance por Região

### 2. Abas Individuais (Hospitais/Parques)
- 4 cards de estatísticas
- 4 gráficos específicos:
  - Distribuição por Tipo
  - Status de Contatos
  - Top 10 Cidades
  - Opera Estacionamento
- Busca em tempo real
- Tabela completa de dados

### 3. Aba de Oportunidades
- Funil de Vendas visual com 4 estágios
- Lista detalhada de oportunidades

---

## 🔄 Atualização de Dados

### Opção 1: Via Interface Web
1. Acesse http://localhost:5000
2. Faça upload da planilha atualizada
3. O dashboard será atualizado automaticamente

### Opção 2: Via Terminal
```bash
python process_excel_dynamic.py "nova_planilha.xlsx"
```

### Opção 3: Substituir Arquivo
1. Substitua o arquivo `Lista Prospecçao.xlsx`
2. Execute: `python process_excel_dynamic.py`

---

## 🌐 URLs Importantes

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Dashboard Principal** | http://localhost:8000/dashboard_completo.html | Visualização dos dados |
| **Interface de Upload** | http://localhost:5000 | Upload de planilhas |
| **Página de Teste** | http://localhost:8000/test_data.html | Teste de carregamento |

---

## ⚙️ Configurações

### Limites de Upload
- **Tamanho máximo**: 50 MB
- **Formatos aceitos**: .xlsx, .xls

Para alterar, edite em `app_upload.py`:
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
```

---

## 🐛 Solução de Problemas

### Erro: "Nenhum módulo chamado 'flask'"
```bash
pip install flask flask-cors
```

### Erro: "Arquivo não encontrado"
Verifique se está no diretório correto:
```bash
cd "D:\Projetos\Dashboard Comercial"
```

### Dashboard não carrega dados
1. Verifique se o arquivo `all_sheets_data.json` existe
2. Execute o processamento:
```bash
python process_excel_dynamic.py
```

### Porta já em uso
Altere a porta em `app_upload.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Mude 5000 para 5001
```

---

## 📝 Notas Importantes

1. **Backup**: Sempre faça backup das planilhas originais antes de processar
2. **Encoding**: Use UTF-8 para caracteres especiais
3. **Performance**: Planilhas com mais de 10.000 linhas podem demorar mais para processar
4. **Cache**: Use Ctrl+F5 no navegador para forçar atualização após upload

---

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs no terminal onde o servidor está rodando
2. Consulte este guia
3. Verifique se todas as dependências estão instaladas

---

## 📜 Histórico de Versões

### v2.0 - Sistema Escalável
- ✅ Detecção automática de abas
- ✅ Interface de upload web
- ✅ Processador dinâmico
- ✅ Dashboard totalmente adaptável

### v1.0 - Versão Inicial
- ✅ Dashboard básico com 6 abas fixas
- ✅ Processamento manual

---

**Desenvolvido com ❤️ para gestão comercial eficiente**
